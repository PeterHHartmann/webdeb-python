from datetime import datetime
from email.policy import default
import time
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
import re, json, os, smtplib, ssl, traceback
from uuid import uuid4
from bottle import error, get, post, redirect, request, response, run, static_file, view, TEMPLATE_PATH, abort
import g
import bcrypt
import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
import db.database as db

import uuid
import imghdr

TEMPLATE_PATH.insert(0, 'public/views')

def set_JWT(payload):
    encoded_jwt = jwt.encode(payload, "secret_jwt", algorithm="HS256")
    cookie_opts = {'max_age': 3600 * 24 * 3}
    response.set_cookie("JWT", json.dumps(encoded_jwt), "secret_info", **cookie_opts)

def get_JWT():
    try:
        cookie = request.get_cookie("JWT", secret="secret_info")
        parsed = json.loads(cookie)
        data = jwt.decode(parsed, key="secret_jwt", algorithms=["HS256"])
        return data
    except:
        return None

def send_validation_email(url, code, user_name):
    sender_email = os.getenv('EMAIL')

    #TODO change receiver_email to the email that signed up
    receiver_email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = "Not Twitter Email Confirmation"
    message["From"] = sender_email
    message["To"] = receiver_email

    #TODO change url to work with pythonanywhere
    full_url = f'http://localhost:3334/auth/{url}'

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi, {user_name}
    Thank you for signing up to Not Twitter.
    Please visit: {full_url} to confirm your email
    Your verification code is: {code}
    """

    html = f"""\
    <html>
        <body>
        <h2 style="color: rgb(29, 155, 240)">Hi, {user_name}.</h2>
        <h3>Thank you for signing up to Not Twitter.</h3>
        <span>
            <p>Your verification code is: </p>
            <h1 style="color: rgb(51, 51, 51)">{code}</h1>
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
        except:
            traceback.print_exc()

### static file routes
@get('/style/<stylesheet_name>')
def _(stylesheet_name):
    return static_file(stylesheet_name, root='public/style')

@get('/js/<script_name>')
def _(script_name):
    return static_file(script_name, root='public/javascript')

@get('/image/<image_name>')
def _(image_name):
    return static_file(image_name, root='public/image')

### views
@get('/')
@view('index')
def _():
    payload = get_JWT()
    if not payload:
        return redirect('/login')

    if request.query.get('signedin'):
        return dict(toast_msg='You have successfully logged in', **payload)
    return payload

@get('/login')
@view('login')
def _():
    cookie = request.get_cookie("JWT", secret="secret_info")
    if cookie:
        parsed = json.loads(cookie)
        data = jwt.decode(parsed, key="secret_jwt", algorithms=["HS256"])
        if data.get('status'):
            return redirect(f'/auth/{data["status"]["url_snippet"]}')
        return redirect('/')
    else:
        return

@post('/login')
def _():
    data = json.load(request.body)
    input = {
        'email': data.get('email'),
        'pwd': data.get('pwd'),
    }
    if not input['email'] or len(input['email'].strip()) < 1:
        response.status = 400
        return dict(msg='Please enter an email')
    if not re.match(g.REGEX_EMAIL, input['email']):
        response.status = 400
        return dict(msg='Please enter a valid email')
    if not input['pwd'] or len(input['pwd'].strip()) < 1:
        response.status = 400
        return dict(msg='Please enter a password')

    try:
        user = db.user_get_by_email(input['email'])

        # check if input pwd doesn't match db password
        if bcrypt.checkpw(bytes(input['pwd'], 'utf-8'), bytes(user['user_pwd'], 'utf-8')):
            details = db.details_get(user_name=user['user_name'])
            payload = {
                'user_name': user['user_name'],
                'user_email': user['user_email'],
                'display_name': details['display_name']
            }
            try:
                # check if user has validated their email 
                # if they haven't return redirect url with error code 403: Forbidden
                validation = db.validation_get_by_email(user['user_email'])
                if validation:
                    payload['status'] = {'verified': False, 'url_snippet': validation['validation_url']}
                    set_JWT(payload)
                    response.status = 403
                    return dict(url_snippet=validation['validation_url'])
            finally:
                set_JWT(payload)
                return
        # otherwise proceed with login process
        else:
            response.status = 401
            return dict(msg='Invalid email or password')
    except:
        traceback.print_exc()
        response.status = 401
        return dict(msg='Invalid email or password')

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
    data = json.load(request.body)

    display_name = data.get('display_name').strip()
    if len(display_name) < 1:
        response.status = 400
        return dict(msg='Please enter a display name')
    if len(display_name) > 50:
        response.status = 400
        return dict(msg='Display name is too long (Maximum 50 characters')

    #TODO no white spaces in username
    user_name = data.get('user_name').strip()
    if len(user_name) < 1:
        response.status = 400
        return dict(msg='Please enter a username')
    if len(user_name) > 50:
        response.status = 400
        return dict(msg='Username is too long (Maximum 50 characters)')

    user_email = data.get('user_email')
    if not re.match(g.REGEX_EMAIL, user_email):
        response.status = 400
        return dict(msg='Please enter a valid email')
    user_pwd = data.get('user_pwd').strip()
    if len(user_pwd) < 6 or len(user_pwd) > 20:
        response.status = 400
        return dict(msg='Password must be longer than 6 or shorter than 20 characters')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(user_pwd, 'utf_8'), salt).decode('utf-8')

    try:
        validation = {
            'code': randint(100000, 999999),
            'url_snippet': str(uuid4())
        }

        print(validation['code'])

        # TODO prettier with something like:
        #   test_user = dict(**data)
        #   print(test_user)
        user = dict(
            user_name=user_name,
            user_email=user_email,
            user_pwd=hashed)

        now = datetime.now()
        joined_month = now.strftime('%B')
        joined_year = int(now.strftime('%Y'))
        details = dict(display_name=display_name, joined_month=joined_month, joined_year=joined_year)

        db.user_post(user, validation, details)
        send_validation_email(validation['url_snippet'], validation['code'], user_name)
        return dict(url_snippet=validation['url_snippet'])
        
    except Exception as e:
        traceback.print_exc()
        response.status = 400
        if str(e) == 'UNIQUE constraint failed: users.user_name':
            return dict(msg='That username is taken')
        elif str(e) == 'UNIQUE constraint failed: users.user_email':
            return dict(msg='That email is already in use')

@get('/logout')
def _():
    response.delete_cookie("JWT", secret="secret_info")
    return redirect('/login')

@get('/auth/<url_code>')
@view('email-validation')
def _(url_code):
    try:
        validation = db.validation_get_by_url(url_code)
        return dict(user_name=validation['user_name'], user_email=validation['user_email'], confirmation_url=url_code)
    except Exception as ex:
        traceback.print_exc()
        return redirect('/signup')

@post('/auth/<url_code>/resend')
def _(url_code):
    data = json.load(request.body)
    try:
        new_code = randint(100000, 999999)
        db.validation_update_code(data['user_email'], new_code)
        send_validation_email(url_code, new_code, data['user_name'])
        return
    except:
        traceback.print_exc()
        response.status = 500
        return dict(msg='something went wrong sorry')

@post('/auth/<url_code>')
def _(url_code):
    data = json.load(request.body)
    try:
        confirmation = db.validation_get_by_url(url_code)
        if confirmation:
            if confirmation['validation_code'] == int(data['code']):
                db.validation_delete(dict(user_email=data['user_email']))

                # try to remove the email validation field on JWT on cookie
                try:
                    cookie = request.get_cookie("JWT", secret="secret_info")
                    parsed = json.loads(cookie)
                    data = jwt.decode(parsed, key="secret_jwt", algorithms=["HS256"])
                    del data['status']
                    encoded_jwt = jwt.encode(data, "secret_jwt", algorithm="HS256")
                    response.set_cookie("JWT", json.dumps(encoded_jwt), "secret_info")
                finally:
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

@get('/user/<user_name>')
@view('user')
def _(user_name):
    payload = get_JWT()
    if not payload:
        return redirect('/login')
    try:
        user = db.user_get_by_username(user_name)
        details = db.details_get(user_name)
        print(details.get('bio'))
        body = dict(
            profile_user_name       =   user['user_name'], 
            profile_display_name    =   details['display_name'], 
            profile_bio             =   details['bio'],
            profile_joined_month    =   details['joined_month'], 
            profile_joined_year     =   details['joined_year'], 
            **payload
        )
        return body
    except:
        traceback.print_exc()
        abort(404)

@get('/user/<user_name>/<identifier>.jpg')
def _(user_name, identifier):
    try:
        user_images = db.details_get_images(user_name)
        stream = BytesIO(user_images[str(identifier)])
        bytes = stream.read()
        response.set_header('Content-Type', 'image/jpeg')
        return bytes
    except:
        traceback.print_exc()
        abort(404)

@post('/user/edit/<user_name>')
def _(user_name):
    payload = get_JWT()
    if not payload:
        return redirect('/login')
    if payload['user_name'] == user_name:
        current_imgs = db.details_get_images(user_name)
        pfp = request.files.get('pfp')
        banner = request.files.get('banner')
        details = {
            'display_name': request.forms.get('display_name'),
            'bio': request.forms.get('bio')
        }
        if pfp:
            details['pfp'] = pfp.file.read()
        else:
            details['pfp'] = current_imgs['pfp']
        if banner:
            details['banner'] = banner.file.read()
        else:
            details['banner'] = current_imgs['banner']
        try:
            db.details_update(user_name, details)
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    else:
        response.status = 403
        return

@error(404)
@view('404')
def _(error):
    return

run(host='127.0.0.1', port=3334, debug=True, reloader=True)