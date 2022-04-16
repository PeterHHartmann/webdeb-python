console.log('signup script loaded');

const remove_errors = (id) => {
    const error_prompt = document.getElementById(id)
    if (error_prompt) {
        error_prompt.remove();
    }
}

document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    remove_errors('signup_error_prompt');
    console.log('signup confirm clicked');
    const data = {
        username: document.getElementById('signup-username').value,
        email: document.getElementById('signup-email').value,
        pwd: document.getElementById('signup-password').value
    }
    const response = await fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    console.log(response);
 
    if ( response.ok ){
        const body = await response.json()
        location = `/auth/${body.url_snippet}`
    } else {
        const body = await response.json()
        console.log(body);
        const error_prompt = document.createElement('span');
        error_prompt.id = 'signup_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = '*' + body.msg;
        document.getElementById('error-container').prepend(error_prompt)
    }
});