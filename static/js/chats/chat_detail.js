document.addEventListener("DOMContentLoaded", () => {
    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;

    const showDetailPlaceholder = (chatPk) => {
        document.querySelectorAll('.chat-detail-placeholder').forEach(placeholder => {
            placeholder.style.display = 'none';
        });

        const detailPlaceholder = document.getElementById(`chat-detail-placeholder-${chatPk}`);
        if (detailPlaceholder) {
            detailPlaceholder.style.display = 'block';
        }
    };

    // If the current URL matches the chat pattern, show the correct placeholder
    if (chatPattern.test(currentPath)) {
        const chatPk = currentPath.match(/\d+/)[0];
        showDetailPlaceholder(chatPk);
    }

    // Set event listener on each chat list item
    document.querySelectorAll('.list-group-item').forEach(item => {
        item.addEventListener('click', () => {
            const chatPk = item.getAttribute('data-chat-pk');
            showDetailPlaceholder(chatPk);
            const url = item.getAttribute("href");
            window.history.pushState(null, "", url); // Update browser history
        });
    });
});
