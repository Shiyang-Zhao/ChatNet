document.addEventListener('DOMContentLoaded', function () {
    const errorDiv = document.getElementById('form-error');

    document.getElementById('group-chat-create-form').addEventListener('submit', function (event) {
        const checkboxes = document.querySelectorAll('.participant-checkbox');
        const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

        if (!isChecked) {
            event.preventDefault();
            // Kill any existing animations on errorDiv before starting new ones
            gsap.killTweensOf(errorDiv);
            errorDiv.style.display = 'block';
            gsap.fromTo(errorDiv, { opacity: 0, y: -10 }, {
                duration: 0.5, opacity: 1, y: 0, ease: "power2.out"
            });

            setTimeout(() => {
                // Start fading out after a delay
                gsap.to(errorDiv, {
                    duration: 0.5, opacity: 0, y: -10, ease: "power2.in", onComplete: function () {
                        errorDiv.style.display = 'none';
                    }
                });
            }, 3000);
        }
    });

    document.querySelectorAll('.participant-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (document.querySelector('.participant-checkbox:checked')) {
                errorDiv.style.display = 'none';
                errorDiv.style.opacity = 0;
                gsap.killTweensOf(errorDiv);
            }
        });
    });
});
