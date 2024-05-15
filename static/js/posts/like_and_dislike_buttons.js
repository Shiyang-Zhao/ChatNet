document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn, .dislike-btn").forEach((button) => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    document.querySelectorAll(".like-form, .dislike-form").forEach((form) => {
        if (form.dataset.listenerAdded === "false") {
            form.addEventListener("submit", (event) => {
                event.preventDefault();
                const postPk = form.dataset.postPk;
                const url = form.dataset.url;
                const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

                axios.post(url, { pk: postPk }, { headers: { "X-CSRFToken": csrfToken } })
                    .then((response) => {
                        console.log(response.data);
                        if (response.data.success) {
                            document.querySelector(`#likes-count-${postPk}`).textContent = response.data.likes_count;
                            document.querySelector(`#dislikes-count-${postPk}`).textContent = response.data.dislikes_count;

                            const likeButton = document.querySelector(`#like-button-${postPk}`);
                            const dislikeButton = document.querySelector(`#dislike-button-${postPk}`);

                            // Reset all buttons to outline
                            likeButton.classList.remove('btn-success');
                            likeButton.classList.add('btn-outline-success');
                            dislikeButton.classList.remove('btn-danger');
                            dislikeButton.classList.add('btn-outline-danger');

                            // Set the appropriate button to solid
                            if (response.data.like_status === 1) {
                                likeButton.classList.add('btn-success');
                                likeButton.classList.remove('btn-outline-success');
                            } else if (response.data.like_status === -1) {
                                dislikeButton.classList.add('btn-danger');
                                dislikeButton.classList.remove('btn-outline-danger');
                            }
                        }
                    });
            });
            form.dataset.listenerAdded = "true";
        }
    });
});
