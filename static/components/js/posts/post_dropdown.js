const handlePostSaveAndUnsaveButton = (container) => {
    container.addEventListener('click', function (event) {
        if (event.target.closest('.post-save-form button') || event.target.closest('.post-unsave-form button')) {
            event.stopPropagation();
        }
    });

    container.addEventListener("submit", function (event) {
        const form = event.target.closest('.post-save-form, .post-unsave-form');
        if (form) {
            event.preventDefault();
            const button = form.querySelector("button");
            const isSaved = form.classList.contains("saved");
            const url = isSaved ? form.getAttribute('data-unsave-url') : form.getAttribute('data-save-url');
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            axios.post(url, {}, {
                headers: { "X-CSRFToken": csrfToken }
            })
                .then((response) => {
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

export { handlePostSaveAndUnsaveButton }