document.addEventListener('DOMContentLoaded', () => {
    let sortSelect = document.querySelector('#sortSelect');

    sortSelect.addEventListener('change', function () {
        window.location.href = this.value;
    });

    document.querySelectorAll('.home-card').forEach(card => {
        card.addEventListener('click', function () {
            window.location.href = this.getAttribute('data-href');
        });
    });

    document.querySelectorAll('.card-author, .file-download-button, .post-toggle-btn').forEach(element => {
        element.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });
});
