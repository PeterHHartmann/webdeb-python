const toggle_modal = (modal_id) => {
    document.getElementById(modal_id).classList.toggle('hidden');
};

const remove_errors = (id) => {
    const error_prompt = document.getElementById(id)
    if (error_prompt) {
        error_prompt.remove();
    }
}

document.getElementById('modal-bg').addEventListener('click', (e) => {
    toggle_modal('modal-mount');
    const modals = document.getElementsByClassName('modal-content')
    for ( let modal of modals){
        if(!modal.classList.contains('hidden')){
            modal.classList.add('hidden')
        }
    }
});

document.getElementById('signup-open').addEventListener('click', (e) => {
    e.preventDefault();
    console.log('signup clicked');
    toggle_modal('modal-mount');
    toggle_modal('signup-modal');
});

document.getElementById('login-open').addEventListener('click', (e) => {
    e.preventDefault();
    console.log('login clicked');
    toggle_modal('modal-mount');
    toggle_modal('login-modal');
});

document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
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
        console.log(body);
        console.log('successfully signed up');
        toggle_modal('modal-mount');
        toggle_modal('signup-modal');
    } else {
        remove_errors('signup_error_prompt');
        const body = await response.json()
        console.log(body);
        const error_prompt = document.createElement('h3');
        error_prompt.id = 'signup_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = body.msg;
        document.getElementById('signup-form').prepend(error_prompt)
    }

});

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
        toggle_modal('modal-mount');
        toggle_modal('login-modal');
        location.reload();
    } else {
        remove_errors('login_error_prompt');
        const body = await response.json()
        console.log(body);
        const error_prompt = document.createElement('h3');
        error_prompt.id = 'login_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = body.msg;
        document.getElementById('login-form').prepend(error_prompt)
    }
});
