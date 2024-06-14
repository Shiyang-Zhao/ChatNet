let socket;
let retryInterval = 1000;
let maxRetryInterval = 60000;

const establishChatWebSocket = (chatPk) => {
    if (socket && socket.readyState === WebSocket.OPEN && socket.chatPk === chatPk) {
        console.log("WebSocket connection already established for this chat.");
        return;
    }

    if (socket) {
        socket.close();
    }
    const socketProtocol =
        window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketURL =
        socketProtocol + window.location.host + `/ws/chats/chat/${chatPk}/`;
    socket = new WebSocket(socketURL);

    socket.chatPk = chatPk;

    socket.onopen = function () {
        console.log("WebSocket connection to chat successfully established!");
        retryInterval = 1000;
    };

    socket.onmessage = function (event) {
        let message = JSON.parse(event.data);
        displayChatItem(message);
        displayMessageItem(message);
    };

    socket.onclose = function (e) {
        console.error(`Chat socket closed: ${e.code}  ${e.reason}`);
    };

    socket.onerror = function (e) {
        console.error(`WebSocket encountered an error: ${e.code}  ${e.reason}`);
        reconnect(chatPk);
    };
};

function reconnect(chatPk) {
    if (socket && socket.chatPk !== chatPk) {
        console.error("WebSocket won't try to reconnect because chat room changed.");
        return;
    }
    console.log(`Attempting to reconnect in ${retryInterval / 1000} seconds...`);
    setTimeout(() => establishChatWebSocket(chatPk), retryInterval);
    retryInterval = Math.min(maxRetryInterval, retryInterval * 2);
};

function sendChatMessage(content) {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.error("WebSocket is not open or not connected");
        return;
    }
    const messageData = {
        type: "chat_message",
        content: content.trim(),
    };
    socket.send(JSON.stringify(messageData));
};

function displayChatItem(message) {
    const chatsList = document.querySelector('#chats-container .chat-list');
    if (chatsList && message.chat_html) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = message.chat_html;
        if (chatsList.firstChild) {
            chatsList.insertBefore(tempDiv, chatsList.firstChild);
        } else {
            chatsList.appendChild(tempDiv);
        }
        gsap.fromTo(tempDiv,
            { opacity: 0, y: -20 },
            { duration: 0.5, opacity: 1, y: 0, ease: 'power2.out' }
        );
    }
}

function displayMessageItem(message) {
    console.log(message)
    const messagesContainer = document.querySelector(
        "#message-detail-placeholder .messages-container"
    );
    if (!messagesContainer) return;
    const messageHtml = message.message_html;
    const isSentByCurrentUser = message.sender_pk == document.body.getAttribute("data-pk");
    console.log(isSentByCurrentUser)
    const tempDiv = document.createElement('div');
    tempDiv.classList.add("message-container", "d-flex", "p-1");
    if (isSentByCurrentUser) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        tempDiv.classList.add("flex-row-reverse");
    }
    tempDiv.innerHTML = messageHtml.trim();
    messagesContainer.appendChild(tempDiv);
};

export { establishChatWebSocket, sendChatMessage }
