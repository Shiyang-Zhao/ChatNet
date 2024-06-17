import { getCookie } from "../../../apps/js/base/base.js";

const handleCommentSaveAndUnsaveButton = (container) => {
    const csrfToken = getCookie('csrftoken');

    container.addEventListener('click', function (event) {
        if (event.target.closest('.comment-save-form button') || event.target.closest('.comment-unsave-form button')) {
            event.stopPropagation();
        }
    });

    container.addEventListener("submit", function (event) {
        const form = event.target.closest('.comment-save-form, .comment-unsave-form');
        if (form) {
            event.preventDefault();
            const button = form.querySelector("button");
            const isSaved = form.classList.contains("saved");
            const url = isSaved ? form.getAttribute('data-unsave-url') : form.getAttribute('data-save-url');

            axios.post(url, {}, {
                headers: { "X-CSRFToken": csrfToken }
            }).then((response) => {
                if (isSaved) {
                    form.classList.remove("saved");
                    form.classList.add("save");
                    button.textContent = "Save";
                    form.action = form.getAttribute("data-save-url");
                } else {
                    form.classList.remove("save");
                    form.classList.add("saved");
                    button.textContent = "Saved";
                    form.action = form.getAttribute("data-unsave-url");
                }
            })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("Something went wrong! Please try again.");
                });
        }
    });
}

export { handleCommentSaveAndUnsaveButton }