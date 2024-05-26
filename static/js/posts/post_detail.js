document.addEventListener("DOMContentLoaded", function () {
    const commentContainer = document.querySelector("#comment-form-container");
    const replyContainers = document.querySelectorAll(".reply-form-container");
    const replyLinks = document.querySelectorAll('.reply-link');
    const commentTextarea = commentContainer.querySelector("textarea");
    const commentButton = commentContainer.querySelector("button");

    commentTextarea.addEventListener("focus", function () {
        gsap.to(commentTextarea, { height: "80px", duration: 0.3 });
        if (commentTextarea.value.trim() !== "") {
            gsap.set(commentButton, { display: 'block' });
            gsap.to(commentButton, { opacity: 1, duration: 0.3, delay: 0.3 });
        }
    });

    commentTextarea.addEventListener("blur", function () {
        gsap.to(commentTextarea, { height: "40px", duration: 0.3 });
        if (commentTextarea.value.trim() === "") {
            gsap.to(commentButton, {
                opacity: 0, duration: 0.3, onComplete: function () {
                    gsap.set(commentButton, { display: 'none' });
                }
            });
        }
    });

    // commentTextarea.addEventListener("input", function () {
    //     if (commentTextarea.value.trim() !== "") {
    //         gsap.set(commentButton, { display: 'block' });
    //         gsap.to(commentButton, { opacity: 1, duration: 0.3 });
    //     } else {
    //         gsap.to(commentButton, {
    //             opacity: 0, duration: 0.3, onComplete: function () {
    //                 gsap.set(commentButton, { display: 'none' });
    //             }
    //         });
    //     }
    // });

    commentTextarea.addEventListener('input', function () {
        if (commentTextarea.value.trim() !== '') {
            gsap.to(commentButton, { x: 0, width: 'auto', autoAlpha: 1, duration: 0.2 });
        } else {
            gsap.to(commentButton, { x: 5, width: 0, autoAlpha: 0, duration: 0.2 });
        }
    });

    commentTextarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            commentContainer.closest('form').submit();
        }
    });

    replyLinks.forEach(function (replyLink) {
        replyLink.addEventListener('click', function () {
            const commentPk = replyLink.getAttribute("data-pk");
            const replyFormWrapper = document.querySelector(`#reply-form-wrapper-${commentPk}`);

            if (replyFormWrapper.style.display === 'none' || replyFormWrapper.style.display === '') {
                gsap.fromTo(replyFormWrapper, { display: 'block', height: 0, opacity: 0 }, { height: 'auto', opacity: 1, duration: 0.3 });
            } else {
                gsap.to(replyFormWrapper, {
                    opacity: 0, height: 0, duration: 0.3, onComplete: function () {
                        replyFormWrapper.style.display = 'none';
                    }
                });
            }
        });
    });

    replyContainers.forEach(function (replyContainer) {
        const textarea = replyContainer.querySelector("textarea");
        const button = replyContainer.querySelector("button");

        textarea.addEventListener("focus", function () {
            gsap.to(textarea, { height: "80px", duration: 0.3 });
            if (textarea.value.trim() !== "") {
                gsap.set(button, { display: 'block' });
                gsap.to(button, { opacity: 1, duration: 0.3, delay: 0.3 });
            }
        });

        textarea.addEventListener('blur', function () {
            gsap.to(textarea, { height: "40px", duration: 0.3 });
            if (textarea.value.trim() === "") {
                gsap.to(button, {
                    opacity: 0, duration: 0.3, onComplete: function () {
                        gsap.set(button, { display: 'none' });
                    }
                });
            }
        });

        // textarea.addEventListener("input", function () {
        //     if (textarea.value.trim() !== "") {
        //         gsap.set(button, { display: 'block' });
        //         gsap.to(button, { opacity: 1, duration: 0.3 });
        //     } else {
        //         gsap.to(button, {
        //             opacity: 0, duration: 0.3, onComplete: function () {
        //                 gsap.set(button, { display: 'none' });
        //             }
        //         });
        //     }
        // });

        textarea.addEventListener('input', function () {
            if (textarea.value.trim() !== '') {
                gsap.to(button, { x: 0, width: 'auto', autoAlpha: 1, duration: 0.2 });
            } else {
                gsap.to(button, { x: 5, width: 0, autoAlpha: 0, duration: 0.2 });
            }
        });

        textarea.addEventListener("keydown", function (e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                replyContainer.closest('form').submit();
            }
        });
    });
});