const toggle_modal = (modal_id) => {
    document.getElementById(modal_id).classList.toggle('hidden');
};

document.getElementById('modal-bg').addEventListener('click', (e) => {
    toggle_modal('modal-mount');
    const modals = document.getElementsByClassName('modal-content')
    for ( let modal of modals){
        if(!modal.classList.contains('hidden')){
            modal.classList.add('hidden')
        }
    }
});

document.getElementById('signup-btn').addEventListener('click', (e) => {
    e.preventDefault();
    console.log('signup clicked');
    toggle_modal('modal-mount');
    toggle_modal('signup-modal');
});

document.getElementById('login-btn').addEventListener('click', (e) => {
    e.preventDefault();
    console.log('signup clicked');
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
        toggle_modal('login-modal');
    } else {

        const body = await response.json()
        console.log(body);
        // if( body.msg == 'invalid password') {
        //     console.log('invalid password');
        // } else if ( body.msg == 'email in use' ) {

        // }
    }

});