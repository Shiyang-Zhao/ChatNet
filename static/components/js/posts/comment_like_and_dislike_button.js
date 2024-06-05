const handleCommentLikeAndDislikeButton = (container) => {
    container.addEventListener('click', function (event) {
        if (event.target.closest('.comment-like-form button') || event.target.closest('.comment-dislike-form button')) {
            event.stopPropagation();
        }
    });

    container.addEventListener('submit', function (event) {
        const form = event.target.closest('.comment-like-form, .comment-dislike-form');
        if (form) {
            event.preventDefault();
            const pk = form.getAttribute('data-pk');
            const url = form.getAttribute('data-url');
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            axios.post(url, { pk: pk }, { headers: { "X-CSRFToken": csrfToken } })
                .then((response) => {
                    const { data } = response;
                    if (data.success) {
                        const likeDislikeContainer = form.closest('.comment-like-dislike-container');
                        const likeIcon = likeDislikeContainer.querySelector('.comment-like-form i');
                        const dislikeIcon = likeDislikeContainer.querySelector('.comment-dislike-form i');

                        likeIcon.querySelector('span').textContent = data.likes_count;
                        dislikeIcon.querySelector('span').textContent = data.dislikes_count;

                        likeIcon.classList.remove('fa-solid');
                        likeIcon.classList.add('fa-regular');
                        dislikeIcon.classList.remove('fa-solid');
                        dislikeIcon.classList.add('fa-regular');

                        if (data.like_status === 1) {
                            likeIcon.classList.remove('fa-regular');
                            likeIcon.classList.add('fa-solid');
                        } else if (data.like_status === -1) {
                            dislikeIcon.classList.remove('fa-regular');
                            dislikeIcon.classList.add('fa-solid');
                        }
                    }
                });
        }
    });
}

export { handleCommentLikeAndDislikeButton }
