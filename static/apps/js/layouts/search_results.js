document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', function (event) {
        if (event.target.matches('.dropdown-btn, .dropdown-btn *, .dropdown-item, .dropdown-menu, .card-author, .file-video, .file-download')) {
            event.stopPropagation();
            return;
        }
        const card = event.target.closest('.result-card');
        if (card) {
            window.location.href = card.getAttribute('data-href');
        }
    });

    document.body.addEventListener('mousedown', function (event) {
        if (event.button === 1) {
            const card = event.target.closest('.result-card');
            if (card) {
                window.open(card.getAttribute('data-href'), '_blank');
            }
        }
    });
});
