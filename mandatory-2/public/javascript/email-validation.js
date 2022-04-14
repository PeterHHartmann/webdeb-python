const remove_errors = (id) => {
    const error_prompt = document.getElementById(id)
    if (error_prompt) {
        error_prompt.remove();
    }
}

document.getElementById('validation-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    remove_errors('login_error_prompt');
    const data = {
        code: document.getElementById('validation-code').value,
        user_email: document.getElementById('validation-email').value
    }
    const response = await fetch(location.pathname, {
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

    if ( response.ok ){
        console.log('successfully validated email');
        location = ('/login')
    } else {
        const body = await response.json()
        console.log(body);
        const error_prompt = document.createElement('span');
        error_prompt.id = 'login_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = body.msg;
        document.getElementById('error-container').prepend(error_prompt)
    }
});