import { handleChatSelection, setChatsContainerEventListener } from "../../../components/js/chats/chat_item.js";
document.addEventListener("DOMContentLoaded", function () {
    const chatsContainer = document.querySelector('#chats-container');
    const messagesContainer = document.querySelector('#messages-container');
    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;

    if (chatPattern.test(currentPath)) {
        const pk = currentPath.match(/\d+/)[0];
        handleChatSelection(currentPath, pk, messagesContainer);
    }

    if (chatsContainer) {
        setChatsContainerEventListener(chatsContainer, messagesContainer);
    }
});

