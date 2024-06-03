import { establishNotificationWebSocket } from "../websockets/notification_websocket.js";

document.addEventListener("DOMContentLoaded", () => {
    establishNotificationWebSocket();


    document.querySelectorAll(".save-unsave-form").forEach((form) => {
        if (form.getAttribute('data-listener-added') === "0") {
            form.addEventListener("submit", function (event) {
                event.preventDefault();
                const button = this.querySelector("button");
                const url = form.action;

                axios.post(url, {}, {
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
                            form.action = form.getAttribute("data-unsave-url");
                        }
                    })
                    .catch((error) => {
                        console.error("Error:", error);
                        alert("Something went wrong! Please try again.");
                    });
            });
            form.setAttribute('data-listener-added', "1");
        }
    });
});