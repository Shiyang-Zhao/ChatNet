const handlePostLikeAndDislikeButton = (container) => {
    container.addEventListener('click', function (event) {
        if (event.target.closest('.post-like-form button') || event.target.closest('.post-dislike-form button')) {
            event.stopPropagation();
        }
    });

    // Delegate submit events to handle likes and dislikes
    container.addEventListener('submit', function (event) {
        const form = event.target.closest('.post-like-form, .post-dislike-form');
        if (form) {
            event.preventDefault();
            const pk = form.getAttribute('data-pk');
            const url = form.getAttribute('data-url');
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            axios.post(url, { pk: pk }, { headers: { "X-CSRFToken": csrfToken } })
                .then((response) => {
                    const { data } = response;
                    if (data.success) {
                        const likeDislikeContainer = form.closest('.post-like-dislike-container');
                        const likeButton = likeDislikeContainer.querySelector('.post-like-form button');
                        const dislikeButton = likeDislikeContainer.querySelector('.post-dislike-form button');

                        likeButton.querySelector('span').textContent = data.likes_count;
                        dislikeButton.querySelector('span').textContent = data.dislikes_count;

                        likeButton.classList.remove('btn-success');
                        likeButton.classList.add('btn-outline-success');
                        dislikeButton.classList.remove('btn-danger');
                        dislikeButton.classList.add('btn-outline-danger');

                        if (data.like_status === 1) {
                            likeButton.classList.add('btn-success');
                            likeButton.classList.remove('btn-outline-success');
                        } else if (data.like_status === -1) {
                            dislikeButton.classList.add('btn-danger');
                            dislikeButton.classList.remove('btn-outline-danger');
                        }
                    }
                });
        }
    });
}

export { handlePostLikeAndDislikeButton }