import { handlePostSaveAndUnsaveButton } from "../../../components/js/posts/post_dropdown.js";
import { handlePostLikeAndDislikeButton } from "../../../components/js/posts/post_like_and_dislike_button.js";
import { handleCommentLikeAndDislikeButton } from "../../../components/js/posts/comment_like_and_dislike_button.js";
import { handleCommentSaveAndUnsaveButton } from "../../../components/js/posts/comment_dropdown.js";

document.addEventListener("DOMContentLoaded", function () {
    const postContainer = document.querySelector('#post-container');
    const commentsContainer = document.querySelector('#comments-container');

    handlePostSaveAndUnsaveButton(postContainer);
    handlePostLikeAndDislikeButton(postContainer);
    handleCommentLikeAndDislikeButton(commentsContainer);
    handleCommentSaveAndUnsaveButton(commentsContainer);

    const commentPattern = /^\/posts\/post\/\d+\/comment\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (commentPattern.test(currentPath)) {
        const pathSegments = currentPath.split('/');
        const pk = pathSegments[pathSegments.length - 2];
        const targetComment = document.querySelector(`#comment-${pk} .comment-item`);
        if (!targetComment) return;
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

    commentsContainer.addEventListener('click', function (event) {
        const actionElement = event.target.closest('.comment-edit-link');
        if (!actionElement) return;
        const commentContainer = actionElement.closest('.comment-container');
        const content = commentContainer.querySelector('p').textContent;
        const container = commentContainer.querySelector('.comment-edit-form-container');
        container.querySelector('textarea').value = content;
    });

    commentsContainer.addEventListener('focus', function (event) {
        const textarea = event.target.closest('textarea');
        if (textarea) {
            gsap.to(textarea, { height: "80px", duration: 0.3 });
        }
    }, true);

    // commentsContainer.addEventListener('blur', function (event) {
    //     const textarea = event.target.closest('textarea');
    //     if (!textarea || textarea.value.trim() !== "") return;

    //     const button = textarea.closest('.comment-create-form-container, .comment-edit-form-container').querySelector('button[type="submit"]');
    //     const newFocusInsideForm = event.relatedTarget && textarea.closest('.comment-create-form-container, .comment-edit-form-container').contains(event.relatedTarget);
    //     gsap.to(textarea, { height: "40px", duration: 0.3 });
    //     if (!newFocusInsideForm) {
    //         gsap.to(button, {
    //             opacity: 0, duration: 0.3, onComplete: function () {
    //                 button.style.visibility = 'hidden';
    //                 button.style.width = 0;
    //             }
    //         });
    //     }
    // }, true);

    commentsContainer.addEventListener('input', function (event) {
        const textarea = event.target.closest('textarea');
        if (!textarea) return;
        const button = textarea.closest('.comment-create-form-container, .comment-edit-form-container').querySelector('button[type="submit"]');
        if (textarea.value.trim() !== '') {
            gsap.to(button, { visibility: 'visible', width: 'auto', opacity: 1, duration: 0.2 });
        } else {
            gsap.to(button, { visibility: 'hidden', width: 0, opacity: 0, duration: 0.2 });
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