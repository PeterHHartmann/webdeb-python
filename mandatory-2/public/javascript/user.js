console.log('user script loaded');

const toggle_modal = (modal_id) => {
    document.getElementById(modal_id).classList.toggle('hidden');
};

document.getElementById('modal-bg').addEventListener('click', (e) => {
    toggle_modal('modal-mount');
});

document.getElementById('edit-profile').addEventListener('click', (e) => {
    e.preventDefault();
    console.log('edit-profile clicked');
    toggle_modal('modal-mount')
});

document.getElementById('close-btn').addEventListener('click', (e) => {
    e.preventDefault()
    console.log('close btn clicked');
    document.getElementById('edit-profile-form').reset();
    toggle_modal('modal-mount')
});

document.getElementById('banner-input').addEventListener('change', (e) => {
    console.log('banner-input changed');
    const image = document.getElementById('current-banner');
    image.src = URL.createObjectURL(e.target.files[0]);
    document.getElementById('placeholder').classList.add('hidden');
    document.getElementById('current-banner').classList.remove('hidden');
});

document.getElementById('pfp-input').addEventListener('change', (e) => {
    console.log('pfp-input changed');

    const image = document.getElementById('current-pfp');
    image.src = URL.createObjectURL(e.target.files[0])

});

document.getElementById('edit-profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const user_name = document.getElementById('user_name_input').value
    const banner_img = document.getElementById('banner-input').files[0]
    const pfp_img = document.getElementById('pfp-input').files[0]

    const data = new FormData()
    data.append('banner', banner_img, 'banner.jpg')
    data.append('pfp', pfp_img, 'pfp.jpg')
    data.append('display_name', document.getElementById('display_name_input').value)
    data.append('bio', document.getElementById('bio_input').value)
    
    const response = await fetch(`/edit/${user_name}/banner`, {
        method: 'POST',
        body: data
    })

    console.log(response);

    // const data = {
    //     user_name: document.getElementById('user_name_input').value,
    //     display_name: document.getElementById('display_name_input').value,
    //     bio: document.getElementById('bio_input').value,
    // }
    // console.log(data);
    // const response = await fetch(`/edit/${data.user_name}`, {
    //     method: 'POST',
    //     credentials: 'same-origin',
    //     mode: 'no-cors',
    //     cache: 'no-cache',
    //     redirect: 'follow',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     referrerPolicy: 'no-referrer',

    //     body: JSON.stringify(data)
    // });
    // console.log(response)




});