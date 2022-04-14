
from dotenv import load_dotenv
load_dotenv()
from uuid import uuid4
from bottle import error, get, post, redirect, request, response, run, static_file, view, TEMPLATE_PATH
import g
import re
import json
import bcrypt
import jwt
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
import db.database as db
import traceback

TEMPLATE_PATH.insert(0, 'public/views')

### static file routes
@get('/style/<stylesheet_name>')
def _(stylesheet_name):
    return static_file(stylesheet_name, root='public/style')

@get('/js/<script_name>')
def _(script_name):
    return static_file(script_name, root='public/javascript')

@get('/images/<image_name>')
def _(image_name):
    return static_file(image_name, root='public/image')

### views
@get('/')
@view('index')
def _():
    cookie = request.get_cookie("JWT", secret="secret_info")
    if cookie:
        parsed = json.loads(cookie)
        data = jwt.decode(parsed, key="secret_jwt", algorithms=["HS256"])
        return data
    else:
        return redirect('/login')


@get('/signup')
@view('signup')
def _():
    cookie = request.get_cookie("JWT", secret="secret_info")
    if cookie:
        return redirect('/')
    else:
        return

@post('/signup')
def _():
    user_id = str(uuid4())
    data = json.load(request.body)
    user_name = data.get('username')
    if len(user_name.strip()) < 1:
        response.status = 400
        return dict(msg='Please enter a username')

    user_email = data.get('email')
    if not re.match(g.REGEX_EMAIL, user_email):
        response.status = 400
        return dict(msg='Please enter a valid email')
    user_pwd = data.get('pwd')
    if len(user_pwd) < 6 or len(user_pwd) > 20:
        response.status = 400
        return dict(msg='Password must be longer than 6 or shorter than 20 characters')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(user_pwd, 'utf_8'), salt).decode('utf-8')

    #TODO send confirmation email
    try:
        validation = {
            'code': randint(100000, 999999),
            'url_snippet': str(uuid4())
        }

        user = dict(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            user_pwd=hashed)
        db.user_post(user, validation)

        sender_email = os.getenv('EMAIL')

        #TODO change receiver_email to the email that signed up
        receiver_email = os.getenv('EMAIL')
        password = os.getenv('EMAIL_PW')

        message = MIMEMultipart("alternative")
        message["Subject"] = "Not Twitter Email Confirmation"
        message["From"] = sender_email
        message["To"] = receiver_email

        full_url = f'http://localhost:3334/auth/{validation["url_snippet"]}'

        # Create the plain-text and HTML version of your message
        text = f"""\
        Hi, {user_name}
        Thank you for signing up to Not Twitter.
        Please visit: {full_url} to confirm your email
        Your confirmation digits are: {validation["code"]}
        """

        html = f"""\
        <html>
            <body>
            <h2 style="color: rgb(29, 155, 240)">Hi, {user['user_name']}.</h2>
            <h3>Thank you for signing up to Not Twitter.</h3>
            <span>
                <p>Your email conformation digits are: </p>
                <h1 style="color: rgb(51, 51, 51)">{validation["code"]}</h1>
            </span>
            <p>Please visit <a href="{full_url}">this link</a> to confirm your email</p>
            </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                return "yes, email sent"
            except Exception as ex:
                print("ex")
                return "uppps... could not send the email"
        
    except Exception as e:
        print(e)
        response.status = 400
        if str(e) == 'UNIQUE constraint failed: users.user_name':
            return dict(msg='That username is taken')
        elif str(e) == 'UNIQUE constraint failed: users.user_email':
            return dict(msg='That email is already in use')

    return dict(
                    user_name=user_name,
                    user_email=user_email,
                )

@get('/login')
@view('login')
def _():
    cookie = request.get_cookie("JWT", secret="secret_info")
    if cookie:
        return redirect('/')
    else:
        return

@post('/login')
def _():
    data = json.load(request.body)
    input_email = data.get('email')
    if not input_email or len(input_email.strip()) < 1:
        response.status = 400
        return dict(msg='Please enter an email')
    if not re.match(g.REGEX_EMAIL, input_email):
        response.status = 400
        return dict(msg='Please enter a valid email')

    input_pwd = data.get('pwd')
    if not input_pwd or len(input_pwd.strip()) < 1:
        response.status = 400
        return dict(msg='Please enter a password')

    try:
        result = json.loads(db.user_get(dict(user_email=input_email)))
        if not bcrypt.checkpw(bytes(input_pwd, 'utf-8'), bytes(result.get('user_pwd'), 'utf-8')):
            response.status = 401
            return dict(msg='Invalid email or password')
        else:
            payload = {
                "user_name": result.get('user_name'),
                "user_email": result.get('user_email')
            }
            encoded_jwt = jwt.encode(payload, "secret_jwt", algorithm="HS256")
            print(encoded_jwt)
            cookie_opts = {'max_age': 3600 * 24 * 3}
            response.set_cookie("JWT", json.dumps(encoded_jwt), "secret_info", **cookie_opts)
            return
    except:
        traceback.print_exc()
        print("didn't find user")
        response.status = 401
        return dict(msg='Invalid email or password')

@get('/logout')
def _():
    response.delete_cookie("JWT", secret="secret_info")
    return redirect('/login')

@get('/auth/<url_code>')
@view('email-validation')
def _(url_code):
    try:
        validation = json.loads(db.validation_get(url_code))[0]
        return dict(user_name=validation['user_name'], user_email=validation['user_email'], confirmation_url=url_code)
    except Exception as ex:
        print(ex)
        return redirect('/signup')

@post('/auth/<url_code>')
def _(url_code):
    data = json.load(request.body)
    try:
        confirmation = json.loads(db.validation_get(url_code))
        if confirmation[0]:
            if confirmation[0]['validation_code'] == int(data['code']):
                db.validation_delete(dict(user_email=data['user_email']))
                return
            else:
                response.status = 401
                return dict(msg='Wrong code please try again')
        else:
            response.status = 401
            return dict(msg='Wrong code please try again')
    except:
        traceback.print_exc()
        response.status = 500
        return dict(msg='Something went wrong, please try again later')

@error(404)
@view('404')
def _(error):
    print(error)
    return


run(host='127.0.0.1', port=3334, debug=True, reloader=True, server='paste')