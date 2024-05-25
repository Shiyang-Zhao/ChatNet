document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".follow-unfollow-form").forEach((form) => {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const button = this.querySelector("button");
      const actionUrl = form.action;

      axios.post(actionUrl, {}, {
        headers: { "X-CSRFToken": this.querySelector('input[name="csrfmiddlewaretoken"]').value }
      })
        .then((response) => {
          if (button.classList.contains("following")) {
            button.classList.remove("btn-secondary", "following");
            button.classList.add("btn-primary", "follow");
            button.textContent = "Follow";
            // Update the form action to follow
            form.action = form.getAttribute("data-follow-url");
          } else {
            button.classList.remove("btn-primary", "follow");
            button.classList.add("btn-secondary", "following");
            button.textContent = "Following";
            // Update the form action to unfollow
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
