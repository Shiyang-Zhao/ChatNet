document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-form, .dislike-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            const postPk = form.dataset.postPk;
            const url = form.dataset.url;
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
            // const iconElement = form.querySelector('button i');

            axios.post(url, { pk: postPk }, { headers: { "X-CSRFToken": csrfToken } })
                .then((response) => {
                    if (response.data.success) {
                        document.querySelector(`#likes-count-${postPk}`).textContent = response.data.likes_count;
                        document.querySelector(`#dislikes-count-${postPk}`).textContent = response.data.dislikes_count;
                        // if (iconElement.classList.contains('fa-regular')) {
                        //     iconElement.classList.remove('fa-regular');
                        //     iconElement.classList.add('fa-solid');
                        // } else {
                        //     iconElement.classList.remove('fa-solid');
                        //     iconElement.classList.add('fa-regular');
                        // }
                    }
                })
                .catch(() => {
                    alert("Error: Could not update post.");
                });
        });
    });
});

