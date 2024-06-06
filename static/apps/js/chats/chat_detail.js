import { establishChatWebSocket } from "../websockets/chat_websocket.js";
import { showMessageDetail } from "./message_detail.js";

document.addEventListener("DOMContentLoaded", function () {
    const chatsContainer = document.querySelector('#chats-container');
    const chatDetailPlaceholders = document.querySelectorAll(".chat-detail-placeholder");
    const chooseChatPlaceholder = document.querySelector("#choose-chat-placeholder");

    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (chatPattern.test(currentPath)) {
        const pk = currentPath.match(/\d+/)[0];
        const currentChatContainer = document.querySelector(`#chat-container-${pk}`);
        highlightChat(currentChatContainer);
        toggleChatDetail(pk);
    }

    if (chatsContainer) {
        chatsContainer.addEventListener("click", (event) => {
            const chatContainer = event.target.closest(".chat-container");
            if (chatContainer) {
                highlightChat(chatContainer);
                const pk = chatContainer.getAttribute("data-pk");
                const detailPlaceholder = toggleChatDetail(pk);

                const url = chatContainer.getAttribute("data-url");
                if (detailPlaceholder) {
                    window.history.pushState(null, "", url);
                }
            }
        });
    }

    function highlightChat(chatContainer) {
        document.querySelectorAll(".chat-container").forEach(container => {
            container.style.backgroundColor = "";
        });
        if (chatContainer) {
            chatContainer.style.backgroundColor = "#f0f0f0";
        }
    }

    function toggleChatDetail(pk) {
        const detailPlaceholder = document.querySelector(`#chat-detail-placeholder-${pk}`);
        if (detailPlaceholder) {
            if (chooseChatPlaceholder) {
                chooseChatPlaceholder.style.display = "none";
            }
            chatDetailPlaceholders.forEach(placeholder => {
                placeholder.style.display = 'none';
            });
            detailPlaceholder.style.display = "block";
            establishChatWebSocket(pk);
            showMessageDetail(detailPlaceholder);
        }

        return detailPlaceholder;
    }
});
