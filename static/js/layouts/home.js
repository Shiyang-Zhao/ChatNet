document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.post-card').forEach(card => {
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
