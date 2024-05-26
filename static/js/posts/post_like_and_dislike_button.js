document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".post-like-btn, .post-dislike-btn").forEach((button) => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    document.querySelectorAll(".post-like-form, .post-dislike-form").forEach((form) => {
        if (form.getAttribute('data-listener-added') === "0") {
            form.addEventListener("submit", (event) => {
                event.preventDefault();
                const pk = form.getAttribute('data-post-pk');
                const url = form.getAttribute('data-url');
                const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

                axios.post(url, { pk: pk }, { headers: { "X-CSRFToken": csrfToken } })
                    .then((response) => {
                        const { data } = response;
                        console.log(data);

                        if (data.success) {
                            document.querySelector(`#post-like-count-${pk}`).textContent = data.likes_count;
                            document.querySelector(`#post-dislike-count-${pk}`).textContent = data.dislikes_count;

                            const likeButton = document.querySelector(`#post-like-button-${pk}`);
                            const dislikeButton = document.querySelector(`#post-dislike-button-${pk}`);

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
            });
            form.setAttribute('data-listener-added', "1");
        }
    });
});
