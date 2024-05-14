import { establishChatWebSocket, sendChatMessage } from "../websockets/chat_websocket.js";

const showDetailPlaceholder = (chatPk) => {
    document
        .querySelectorAll(".chat-detail-placeholder")
        .forEach((placeholder) => {
            placeholder.style.display = "none";
        });

    const detailPlaceholder = document.getElementById(
        `chat-detail-placeholder-${chatPk}`
    );
    if (detailPlaceholder) {
        detailPlaceholder.style.display = "block";
        establishChatWebSocket(chatPk);

        const messageInput = detailPlaceholder.querySelector("#messageInput");
        messageInput.scrollIntoView({ behavior: "smooth", block: "nearest" });
        const sendButton = detailPlaceholder.querySelector("#sendButton");

        sendButton.addEventListener("click", () => {
            const messageContent = messageInput.value.trim();
            if (messageContent !== "") {
                sendChatMessage(messageContent);
                messageInput.value = "";
            } else {
                alert("You can't send an empty message");
            }
        });

        messageInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                const messageContent = messageInput.value.trim();
                if (messageContent !== "") {
                    sendChatMessage(messageContent);
                    messageInput.value = "";
                } else {
                    alert("You can't send an empty message");
                }
            }
        });
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (chatPattern.test(currentPath)) {
        const chatPk = currentPath.match(/\d+/)[0];
        showDetailPlaceholder(chatPk);
    }

    document.querySelectorAll(".list-group-item").forEach((item) => {
        item.addEventListener("click", () => {
            const chatPk = item.getAttribute("data-chat-pk");
            showDetailPlaceholder(chatPk);
            const url = item.getAttribute("data-href");
            window.history.pushState(null, "", url);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const modalButton = document.getElementById('openModalButton');
    const myModal = new bootstrap.Modal(document.getElementById('myModal'), {
        keyboard: false
    });

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('group_chat_create_form') === 'open') {
        myModal.show();
    }

    modalButton.addEventListener('click', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('group_chat_create_form', 'open');
        window.history.pushState({}, '', window.location.pathname + '?' + urlParams.toString());
        myModal.show();
    });
});

