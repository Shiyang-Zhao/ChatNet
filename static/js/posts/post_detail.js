document.addEventListener("DOMContentLoaded", function () {
    const commentFormContainer = document.querySelector("#comment-form-container");
    const commentFormTextarea = commentFormContainer.querySelector("textarea");
    const commentFormButton = commentFormContainer.querySelector("button");
    const replyContainers = document.querySelectorAll(".reply-form-container");
    const replyLinks = document.querySelectorAll('.reply-link');

    const commentPattern = /^\/posts\/post\/\d+\/comment\/\d+\/$/;
    const currentPath = window.location.pathname;

    if (commentPattern.test(currentPath)) {
        const pathSegments = currentPath.split('/');
        const commentPk = pathSegments[pathSegments.length - 2];
        const targetComment = document.querySelector(`#comment-item-${commentPk}`);
        if (targetComment) {
            targetComment.scrollIntoView({ behavior: 'smooth' });
            gsap.fromTo(targetComment,
                { backgroundColor: "#ffffff" }, // Start color (white)
                {
                    backgroundColor: "#f0f0f0", // Blink color
                    repeat: 5,
                    yoyo: true,
                    duration: 0.8,
                    ease: "power1.inOut",
                    onComplete: function () {
                        gsap.to(targetComment, { backgroundColor: "#ffffff", duration: 0.8 }); // Ensure it ends on white
                    }
                }
            );
        }
    }

    commentFormTextarea.addEventListener("focus", function () {
        gsap.to(commentFormTextarea, { height: "80px", duration: 0.3 });
        if (commentFormTextarea.value.trim() !== "") {
            gsap.set(commentFormButton, { display: 'block' });
            gsap.to(commentFormButton, { opacity: 1, duration: 0.3, delay: 0.3 });
        }
    });

    commentFormTextarea.addEventListener("blur", function () {
        gsap.to(commentFormTextarea, { height: "40px", duration: 0.3 });
        if (commentFormTextarea.value.trim() === "") {
            gsap.to(commentFormButton, {
                opacity: 0, duration: 0.3, onComplete: function () {
                    gsap.set(commentFormButton, { display: 'none' });
                }
            });
        }
    });

    // commentFormTextarea.addEventListener("input", function () {
    //     if (commentFormTextarea.value.trim() !== "") {
    //         gsap.set(commentFormButton, { display: 'block' });
    //         gsap.to(commentFormButton, { opacity: 1, duration: 0.3 });
    //     } else {
    //         gsap.to(commentFormButton, {
    //             opacity: 0, duration: 0.3, onComplete: function () {
    //                 gsap.set(commentFormButton, { display: 'none' });
    //             }
    //         });
    //     }
    // });

    commentFormTextarea.addEventListener('input', function () {
        if (commentFormTextarea.value.trim() !== '') {
            gsap.to(commentFormButton, { x: 0, width: 'auto', autoAlpha: 1, duration: 0.2 });
        } else {
            gsap.to(commentFormButton, { x: 5, width: 0, autoAlpha: 0, duration: 0.2 });
        }
    });

    commentFormTextarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            commentFormContainer.closest('form').submit();
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