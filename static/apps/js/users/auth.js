document.addEventListener('DOMContentLoaded', function () {
    let authModal = document.querySelector('#authModal');
    const myModal = new bootstrap.Modal(authModal, {
        keyboard: false
    });
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('modal') === 'auth') {
        myModal.show();
    }

    authModal.addEventListener('shown.bs.modal', function () {
        let url = new URL(window.location);
        url.searchParams.set('modal', 'auth');
        window.history.pushState({}, '', url);
    });

    authModal.addEventListener('hidden.bs.modal', function () {
        let url = new URL(window.location);
        url.searchParams.delete('modal');
        window.history.pushState({}, '', url);
    });
});