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

// import { handleStoryShowAndHideButton } from "../../../components/js/stories/story_item.js";

// document.addEventListener("DOMContentLoaded", () => {
//   const storyContainer = document.querySelector('#story-container');
//   const userProfileContainer = document.querySelector('#user-profile-container');
//   handleStoryShowAndHideButton(storyContainer);
//   userProfileContainer.addEventListener("submit", function (event) {
//     const form = event.target.closest('.user-follow-form, .user-unfollow-form, .send-message-form');
//     if (form) {
//       event.preventDefault();
//       const button = form.querySelector("button");
//       const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
//       if (form.classList.contains("user-follow-form") || form.classList.contains("user-unfollow-form")) {
//         const isFollowed = form.classList.contains("following");
//         const url = isFollowed ? form.getAttribute('data-unfollow-url') : form.getAttribute('data-follow-url');

//         axios.post(url, {}, {
//           headers: { "X-CSRFToken": csrfToken }
//         }).then((response) => {
//           if (isFollowed) {
//             form.classList.remove("following");
//             form.classList.add("follow");
//             button.classList.remove("btn-secondary");
//             button.classList.add("btn-primary");
//             button.textContent = "Follow";
//           } else {
//             form.classList.remove("follow");
//             form.classList.add("following");
//             button.classList.remove("btn-primary");
//             button.classList.add("btn-secondary");
//             button.textContent = "Following";
//           }
//         }).catch((error) => {
//           console.error("Error:", error);
//           alert("Something went wrong! Please try again.");
//         });
//       } else if (form.classList.contains("send-message-form")) {
//         const url = form.getAttribute('data-url');
//         const receiverUsername = form.getAttribute("data-receiver-username");
//         axios.post(url, { receiver_username: receiverUsername }, {
//           headers: {
//             "X-CSRFToken": csrfToken,
//             'X-Requested-With': 'XMLHttpRequest',
//           }
//         }).then((response) => {
//           const data = response.data;
//           console.log('Message sent successfully:', response.data);
//           if (data.status === 'created') {
//             const html = data.html;
//             console.log(html)
//           }
//           window.location.href = data.url;
//         }).catch((error) => {
//           console.error("Error:", error);
//           alert("Failed to send message.");
//         });
//       }
//     }
//   });
// });

