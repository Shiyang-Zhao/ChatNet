document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".comment-like-btn, .comment-dislike-btn").forEach((button) => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    document.querySelectorAll(".comment-like-form, .comment-dislike-form").forEach((form) => {
        if (form.getAttribute('data-listener-added') === "0") {
            form.addEventListener("submit", (event) => {
                event.preventDefault();
                const pk = form.getAttribute('data-comment-pk');
                const url = form.getAttribute('data-url');
                const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

                axios.post(url, { pk: pk }, { headers: { "X-CSRFToken": csrfToken } })
                    .then((response) => {
                        const { data } = response;
                        console.log(data);
                        if (data.success) {
                            document.querySelector(`#comment-like-count-${pk}`).textContent = data.likes_count;
                            document.querySelector(`#comment-dislike-count-${pk}`).textContent = data.dislikes_count;

                            const likeIcon = document.querySelector(`#comment-like-button-${pk} i`);
                            const dislikeIcon = document.querySelector(`#comment-dislike-button-${pk} i`);

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
            });
            form.setAttribute('data-listener-added', "1");
        }
    });
});
