document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.following, .follow').forEach(button => {
        button.addEventListener('click', function () {
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            const actionUrl = this.dataset.actionUrl;

            axios.post(actionUrl, {}, { headers: { 'X-CSRFToken': csrfToken } })
                .then(response => {
                    if (this.classList.contains('following')) {
                        this.classList.remove('btn-secondary', 'following');
                        this.classList.add('btn-primary', 'follow');
                        this.textContent = 'Follow';
                        // Update the action URL to follow
                        this.dataset.actionUrl = this.dataset.followUrl;
                    } else {
                        this.classList.remove('btn-primary', 'follow');
                        this.classList.add('btn-secondary', 'following');
                        this.textContent = 'Following';
                        // Update the action URL to unfollow
                        this.dataset.actionUrl = this.dataset.unfollowUrl;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Something went wrong! Please try again.');
                });
        });
    });
});
