import { establishChatWebSocket } from "../websockets/chat_websocket.js";
import { showMessageDetail } from "./message_detail.js";

const showDetailPlaceholder = (chatPk) => {
    document.querySelectorAll(".chat-detail-placeholder").forEach((placeholder) => {
        placeholder.style.display = "none";
    });
    const detailPlaceholder = document.querySelector(
        `#chat-detail-placeholder-${chatPk}`
    );
    if (detailPlaceholder) {
        detailPlaceholder.style.display = "block";
        establishChatWebSocket(chatPk);
        showMessageDetail(detailPlaceholder, chatPk);
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (chatPattern.test(currentPath)) {
        const chatPk = currentPath.match(/\d+/)[0];
        showDetailPlaceholder(chatPk);
    }

    document.querySelectorAll(".chat-item").forEach((item) => {
        item.addEventListener("click", () => {
            const chatPk = item.getAttribute("data-chat-pk");
            showDetailPlaceholder(chatPk);
            const url = item.getAttribute("data-href");
            if (document.querySelector(`#chat-detail-placeholder-${chatPk}`)) {
                window.history.pushState(null, "", url);
            }
        });
    });
});
