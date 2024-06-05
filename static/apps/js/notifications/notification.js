document.addEventListener('DOMContentLoaded', function () {
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
    const markAllAsReadForm = document.querySelector('.mark-all-as-read-form')
    markAllAsReadForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const url = markAllAsReadForm.getAttribute('data-url');
        const csrfToken = markAllAsReadForm.querySelector('input[name="csrfmiddlewaretoken"]').value;
        axios.post(url, {}, {
            headers: { 'X-CSRFToken': csrfToken }
        }).then(response => {
            document.querySelectorAll('.card-body').forEach(cardBody => {
                cardBody.style.backgroundColor = '';
            });
            countElement.textContent = '';
            countElement.style.display = 'none';
        })
    });

    const notificationsContainer = document.querySelector('#notifications-container');

    notificationsContainer.addEventListener('submit', function (event) {
        event.preventDefault();
        const form = event.target.closest('.mark-as-read-form, .mark-as-unread-form');
        const url = form.getAttribute('data-url');
        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

        axios.post(url, {}, {
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
