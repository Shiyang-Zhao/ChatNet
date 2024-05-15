document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn, .dislike-btn").forEach((button) => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    })

    document.querySelectorAll(".like-form, .dislike-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            const postPk = form.dataset.postPk;
            const url = form.dataset.url;
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            axios.post(url, { pk: postPk }, { headers: { "X-CSRFToken": csrfToken } })
                .then((response) => {
                    console.log(response.data)
                    if (response.data.success) {
                        document.querySelector(`#likes-count-${postPk}`).textContent = response.data.likes_count;
                        document.querySelector(`#dislikes-count-${postPk}`).textContent = response.data.dislikes_count;

                        const likeButoon = document.querySelector(`#like-button-${postPk}`);
                        const dislikeButton = document.querySelector(`#dislike-button-${postPk}`);

                        if (response.data.like_status === 1) {
                            likeButoon.style.backgroundColor = '#198754';
                            likeButoon.style.color = '#ffffff';
                            dislikeButton.style.backgroundColor = '';
                            dislikeButton.style.color = '';
                        } else if (response.data.like_status === -1) {
                            dislikeButton.style.backgroundColor = '#dc3545';
                            dislikeButton.style.color = '#ffffff'
                            likeButoon.style.backgroundColor = '';
                            likeButoon.style.color = '';
                        }
                    }
                });
        });
    });
});

