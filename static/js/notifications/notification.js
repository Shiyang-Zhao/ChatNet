document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const countElement = document.querySelector("#notification-count");

    const updateUnreadNotificationCount = (direction) => {
        let unreadCount = parseInt(countElement.textContent) || 0;
        unreadCount += direction;
        if (unreadCount > 0) {
            countElement.textContent = unreadCount;
            countElement.style.display = 'inline-block';
        } else {
            countElement.textContent = '';
            countElement.style.display = 'none';
        }
    };

    document.querySelector('#mark-all-as-read-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const url = this.action;

        axios.post(url, null, {
            headers: { 'X-CSRFToken': csrfToken }
        }).then(response => {
            document.querySelectorAll('.card-body').forEach(cardBody => {
                cardBody.style.backgroundColor = '';
            });
            countElement.textContent = '';
            countElement.style.display = 'none';
        })
    });

    document.querySelector('#notification-list').addEventListener('submit', function (event) {
        event.preventDefault();
        const form = event.target;
        const url = form.getAttribute('data-url');

        axios.post(url, null, {
            headers: { 'X-CSRFToken': csrfToken }
        }).then(response => {
            const cardBody = form.closest('.card-body');
            if (form.classList.contains('mark-as-read-form')) {
                cardBody.style.backgroundColor = '';
                updateUnreadNotificationCount(-1);
            } else if (form.classList.contains('mark-as-unread-form')) {
                cardBody.style.backgroundColor = '#f0f0f0';
                updateUnreadNotificationCount(1);
            }
        })
    });
});
