document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.post-card').forEach(card => {
        card.addEventListener('click', function () {
            window.location.href = this.getAttribute('data-href');
        });
    });

    document.querySelectorAll('.card-author').forEach(card => {
        card.addEventListener('click', function () {
            event.stopPropagation();
        });
    });
});
