const remove_errors = (id) => {
    const error_prompt = document.getElementById(id)
    if (error_prompt) {
        error_prompt.remove();
    }
}

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('login confirm clicked');

    const data = {
        email: document.getElementById('login-email').value,
        pwd: document.getElementById('login-password').value
    }
    const response = await fetch('/login', {
        method: 'POST',
        credentials: 'same-origin',
        mode: 'no-cors',
        cache: 'no-cache',
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json'
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
    console.log(response);

    if ( response.ok ){
        console.log('successfully logged in');
        location = '/';
    } else {
        remove_errors('login_error_prompt');
        const body = await response.json()
        console.log(body);
        const error_prompt = document.createElement('span');
        error_prompt.id = 'login_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = '* ' + body.msg;
        document.getElementById('error-container').prepend(error_prompt)
    }
});