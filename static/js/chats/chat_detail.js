import { establishWebSocket, sendMessage } from "./websocket.js";

const chatPattern = /^\/chats\/chat\/\d+\/$/;
let messageInput;
let sendButton;

const showDetailPlaceholder = (chatPk) => {
    document.querySelectorAll('.chat-detail-placeholder').forEach(placeholder => {
        placeholder.style.display = 'none';
    });

    const detailPlaceholder = document.getElementById(`chat-detail-placeholder-${chatPk}`);
    if (detailPlaceholder) {
        detailPlaceholder.style.display = 'block';
        establishWebSocket(chatPk);

        messageInput = detailPlaceholder.querySelector("#messageInput");
        sendButton = detailPlaceholder.querySelector("#sendButton");


        sendButton.addEventListener('click', () => {
            if (messageInput.value.trim() !== '') {
                sendMessage({ content: messageInput.value.trim() });
                messageInput.value = '';
            } else {
                alert("fuck you")
            }
        });

        messageInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                if (messageInput.value.trim() !== '') { // Check if the form is valid
                    sendMessage({ content: messageInput.value.trim() });
                    messageInput.value = '';
                } else {
                    alert("fuck you")
                }
            }
        });
    }
};

const currentPath = window.location.pathname;
if (chatPattern.test(currentPath)) {
    const chatPk = currentPath.match(/\d+/)[0];
    showDetailPlaceholder(chatPk);
}

document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('click', () => {
        const chatPk = item.getAttribute('data-chat-pk');
        showDetailPlaceholder(chatPk);
        const url = item.getAttribute("data-href");
        window.history.pushState(null, "", url);
    });
});
