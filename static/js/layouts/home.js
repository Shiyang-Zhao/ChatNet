document.addEventListener('DOMContentLoaded', () => {
    let sortSelect = document.querySelector('#sortSelect');

    sortSelect.addEventListener('change', function () {
        window.location.href = this.value;
    });

    document.querySelectorAll('.home-card').forEach(card => {
        card.addEventListener('click', function () {
            window.location.href = this.getAttribute('data-href');
        });
    });

    document.querySelectorAll('.card-author, .file-download-button, .dropdown-btn, .dropdown-item').forEach(element => {
        element.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    document.querySelectorAll(".save-unsave-form").forEach((form) => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            const button = this.querySelector("button");
            const actionUrl = form.action;

            axios.post(actionUrl, {}, {
                headers: { "X-CSRFToken": this.querySelector('input[name="csrfmiddlewaretoken"]').value }
            })
                .then((response) => {
                    if (button.classList.contains("saved")) {
                        button.classList.remove("saved");
                        button.classList.add("save");
                        button.textContent = "Save";
                        form.action = form.getAttribute("data-save-url");
                    } else {
                        button.classList.remove("save");
                        button.classList.add("saved");
                        button.textContent = "Saved";
                        form.action = form.getAttribute("data-unfollow-url");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("Something went wrong! Please try again.");
                });
        });
    });
});
