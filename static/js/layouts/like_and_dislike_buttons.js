document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn, .dislike-btn').forEach(button => {
        button.addEventListener('click', () => {
            const { postPk, url } = button.dataset;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            axios.post(url, { pk: postPk }, { headers: { 'X-CSRFToken': csrfToken } })
                .then(response => {
                    if (response.data.success) {
                        document.querySelector(`#likes-count-${postPk}`).textContent = `${response.data.likes_count} Likes`;
                        document.querySelector(`#dislikes-count-${postPk}`).textContent = `${response.data.dislikes_count} Dislikes`;
                    }
                })
                .catch(() => {
                    alert('Error: Could not update post.');
                });
        });
    });
});
