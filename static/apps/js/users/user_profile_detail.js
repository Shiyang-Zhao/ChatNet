import { handleStoryShowAndHideButton } from "../../../components/js/stories/story_item.js";

document.addEventListener("DOMContentLoaded", () => {
  const storyContainer = document.querySelector('#story-container');
  const userProfileContainer = document.querySelector('#user-profile-container');
  handleStoryShowAndHideButton(storyContainer);
  userProfileContainer.addEventListener("submit", function (event) {
    const form = event.target.closest('.user-follow-form, .user-unfollow-form');
    if (form) {
      event.preventDefault();
      const button = form.querySelector("button");
      const isFollowed = form.classList.contains("following");
      const url = isFollowed ? form.getAttribute('data-unfollow-url') : form.getAttribute('data-follow-url');
      const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

      axios.post(url, {}, {
        headers: { "X-CSRFToken": csrfToken }
      })
        .then((response) => {
          if (isFollowed) {
            form.classList.remove("following");
            form.classList.add("follow");
            button.classList.remove("btn-secondary");
            button.classList.add("btn-primary");
            button.textContent = "Follow";
          } else {
            form.classList.remove("follow");
            form.classList.add("following");
            button.classList.remove("btn-primary");
            button.classList.add("btn-secondary");
            button.textContent = "Following";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Something went wrong! Please try again.");
        });
    }
  });
});
