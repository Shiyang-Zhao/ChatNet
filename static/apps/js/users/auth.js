document.addEventListener('DOMContentLoaded', function () {
    let authModal = document.querySelector('#authModal');
    const myModal = new bootstrap.Modal(authModal, {
        keyboard: false
    });

    const urlParams = new URLSearchParams(window.location.search);
    let modalType = urlParams.get('modal');

    if (modalType === 'login' || modalType === 'signup') {
        myModal.show();
        const tabToShow = modalType === 'login' ? '#login-tab' : '#signup-tab';
        const tab = new bootstrap.Tab(document.querySelector(tabToShow));
        tab.show();
    }

    authModal.addEventListener('shown.bs.modal', function () {
        if (!modalType) {
            modalType = document.querySelector('.nav-link.active').getAttribute('data-target');
        }
        let url = new URL(window.location);
        url.searchParams.set('modal', modalType);
        window.history.pushState({}, '', url);
    });

    authModal.addEventListener('hidden.bs.modal', function () {
        let url = new URL(window.location);
        url.searchParams.delete('modal');
        window.history.pushState({}, '', url);
    });

    authModal.querySelectorAll('[data-bs-toggle="tab"]').forEach(function (tab) {
        tab.addEventListener('shown.bs.tab', function (event) {
            modalType = event.target.getAttribute('data-target');
            let url = new URL(window.location);
            url.searchParams.set('modal', modalType);
            window.history.pushState({}, '', url);
        });
    });
});
