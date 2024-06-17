document.querySelector('#file-input').addEventListener('change', function (event) {
    const file = event.target.files[0];
    const imagePreview = document.querySelector('#image-preview');
    const videoPreview = document.querySelector('#video-preview');

    imagePreview.style.display = 'none';
    videoPreview.style.display = 'none';
    imagePreview.src = '';
    videoPreview.src = '';

    if (file) {
        const fileURL = URL.createObjectURL(file);
        if (file.type.startsWith('image/')) {
            imagePreview.src = fileURL;
            imagePreview.style.display = 'block';
        } else if (file.type.startsWith('video/')) {
            videoPreview.src = fileURL;
            videoPreview.style.display = 'block';
        }
    }
});