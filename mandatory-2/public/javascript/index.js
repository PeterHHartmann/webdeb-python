const auto_grow = (element) => {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

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

window.addEventListener('load', () => {
    const toast = document.querySelector('toast')
    toast.classList.remove('hidden')
    requestAnimationFrame(() => {
        toast.classList.add('showing')
    });
    setTimeout(() => {
        requestAnimationFrame(() => {
            toast.classList.remove('showing')
            toast.classList.remove('hidden')
        })
    }, 2500);
})