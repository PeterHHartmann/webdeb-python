const remove_errors = (id) => {
    const error_prompt = document.getElementById(id)
    if (error_prompt) {
        error_prompt.remove();
    }
}

const toggle_spinner = () => {
    document.querySelector(`#submit-text`).classList.toggle('hidden')
    document.querySelector('.spinner').classList.toggle('hidden')
}

document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    toggle_spinner()
    remove_errors('login_error_prompt');
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

    if ( response.ok ){
        location = '/?signedin=true'
    } else if (response.status === 403){
        const body = await response.json()
        location = `auth/${body.url_snippet}`
    } else {
        const body = await response.json()
        const error_prompt = document.createElement('span');
        error_prompt.id = 'login_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = '* ' + body.msg;
        document.getElementById('error-container').prepend(error_prompt);
        document.getElementById('login-password').value = '';
    }
    toggle_spinner();
});