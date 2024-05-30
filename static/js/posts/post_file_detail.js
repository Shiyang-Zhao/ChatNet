document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.file-video, .file-download').forEach(element => {
        element.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });
});
