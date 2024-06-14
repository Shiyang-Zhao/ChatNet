import { handleChatSelection, handleChatsContainerEventListener } from "../../../components/js/chats/chat_item.js";
document.addEventListener("DOMContentLoaded", function () {
    const chatsContainer = document.querySelector('#chats-container');
    const chatDetailPlaceholder = document.querySelector('#message-detail-placeholder');
    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;

    if (chatPattern.test(currentPath)) {
        const pk = currentPath.match(/\d+/)[0];
        handleChatSelection(currentPath, pk, chatDetailPlaceholder);
    }

    if (chatsContainer) {
        handleChatsContainerEventListener(chatsContainer, chatDetailPlaceholder);
    }
});

