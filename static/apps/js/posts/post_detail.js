import { handlePostSaveAndUnsaveButton } from "../../../components/js/posts/post_dropdown.js";
import { handlePostLikeAndDislikeButton } from "../../../components/js/posts/post_like_and_dislike_button.js";
import { handleCommentLikeAndDislikeButton } from "../../../components/js/posts/comment_like_and_dislike_button.js";

document.addEventListener("DOMContentLoaded", function () {
    const postContainer = document.querySelector('#post-container');
    const commentsContainer = document.querySelector('#comments-container');

    handlePostSaveAndUnsaveButton(postContainer);
    handlePostLikeAndDislikeButton(postContainer);
    handleCommentLikeAndDislikeButton(commentsContainer);

    const commentPattern = /^\/posts\/post\/\d+\/comment\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (commentPattern.test(currentPath)) {
        const pathSegments = currentPath.split('/');
        const commentPk = pathSegments[pathSegments.length - 2];
        const targetComment = document.querySelector(`#comment-${commentPk}`);
        if (targetComment) {
            targetComment.scrollIntoView({ behavior: 'smooth' });
            gsap.fromTo(targetComment,
                { backgroundColor: "#ffffff" },
                {
                    backgroundColor: "#aaaaaa",
                    repeat: 5,
                    yoyo: true,
                    duration: 0.8,
                    ease: "power1.inOut",
                    onComplete: function () {
                        gsap.to(targetComment, { backgroundColor: "#ffffff", duration: 0.8 });
                    }
                }
            );
        }
    }

    commentsContainer.addEventListener('click', function (event) {
        const actionElement = event.target.closest('.comment-form-container, .reply-link');
        if (!actionElement) return;

        if (actionElement.classList.contains('reply-link')) {
            const container = actionElement.closest('.comment-container').querySelector('.comment-form-container');

            if (!container.style.display || container.style.display === 'none') {
                gsap.fromTo(container, { display: 'block', height: 0, opacity: 0 }, {
                    height: 'auto', opacity: 1, duration: 0.3, onComplete: () => {
                        container.querySelector('textarea').focus();
                    }
                });
            } else {
                gsap.to(container, {
                    opacity: 0, height: 0, duration: 0.3, onComplete: function () {
                        container.style.display = 'none';
                    }
                });
            }
        } else if (actionElement.classList.contains('comment-form-container')) {
            const textarea = actionElement.querySelector('textarea');
            const button = actionElement.querySelector('button[type="submit"]');
            if (textarea && textarea.value.trim() !== '') {
                gsap.to(button, { visibility: 'visible', width: 'auto', opacity: 1, duration: 0.2 });
            }
        }
    });

    commentsContainer.addEventListener('focus', function (event) {
        const textarea = event.target.closest('textarea');
        if (textarea) {
            gsap.to(textarea, { height: "80px", duration: 0.3 });
        }
    }, true);

    commentsContainer.addEventListener('blur', function (event) {
        const textarea = event.target.closest('textarea');
        if (!textarea) return;

        const button = textarea.closest('.comment-form-container').querySelector('button[type="submit"]');
        const newFocusInsideForm = event.relatedTarget && textarea.closest('.comment-form-container').contains(event.relatedTarget);
        if (textarea.value.trim() === "") {
            gsap.to(textarea, { height: "40px", duration: 0.3 });  // Reduce height only if empty
            if (!newFocusInsideForm) {
                gsap.to(button, {
                    opacity: 0, duration: 0.3, onComplete: function () {
                        button.style.visibility = 'hidden';
                        button.style.width = 0;
                    }
                });
            }
        }
    }, true);

    commentsContainer.addEventListener('input', function (event) {
        const textarea = event.target.closest('textarea');
        if (textarea) {
            const button = textarea.closest('.comment-form-container').querySelector('button[type="submit"]');
            if (textarea.value.trim() !== '') {
                gsap.to(button, { visibility: 'visible', width: 'auto', opacity: 1, duration: 0.2 });
            } else {
                gsap.to(button, { visibility: 'hidden', width: 0, opacity: 0, duration: 0.2 });
            }
        }
    });

    commentsContainer.addEventListener('keydown', function (event) {
        if (event.target.tagName === 'TEXTAREA' && event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            const form = event.target.closest('form');
            if (form) {
                form.submit();
            }
        }
    });
});