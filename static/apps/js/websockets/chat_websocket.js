let socket;
let retryInterval = 1000;
let maxRetryInterval = 60000;
let sessionId = generateSessionId();
let connectionId = generateConnectionId();

const establishChatWebSocket = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        console.log("WebSocket connection already established.");
        return;
    }

    const socketProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketURL = `${socketProtocol}${window.location.host}/ws/chats/?sid=${sessionId}&cid=${connectionId}`;
    socket = new WebSocket(socketURL);

    socket.onopen = function () {
        console.log("WebSocket connection to chat successfully established!");
        console.log(`Session ID: ${sessionId}, Connection ID: ${connectionId}`);
        retryInterval = 1000;
    };

    socket.onmessage = function (event) {
        const message = JSON.parse(event.data);
        displayMessageItem(message);
        console.log(message);
    };

    socket.onclose = function (e) {
        console.error(`WebSocket closed: ${e.code} ${e.reason}`);
        reconnect();
    };

    socket.onerror = function (e) {
        console.error(`WebSocket encountered an error: ${e.message}`);
        reconnect();
    };
};

function reconnect() {
    console.log(`Attempting to reconnect in ${retryInterval / 1000} seconds...`);
    setTimeout(establishChatWebSocket, retryInterval);
    retryInterval = Math.min(maxRetryInterval, retryInterval * 2);
}

function generateSessionId() {
    return 'xxxx-xxxx-xxxx'.replace(/[x]/g, () => {
        return Math.floor(Math.random() * 16).toString(16);
    });
}

function generateConnectionId() {
    return 'xxxx-xxxx-xxxx'.replace(/[x]/g, () => {
        return Math.floor(Math.random() * 16).toString(16);
    });
}

function sendChatMessage(chatPk, content) {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.error("WebSocket is not open or not connected");
        return;
    }
    const payload = {
        type: "chat_message",
        chat_pk: chatPk,
        content: content.trim(),
        sid: sessionId,
        cid: connectionId
    };
    socket.send(JSON.stringify(payload));
}

function displayMessageItem(message) {
    const messagesContainer = document.querySelector("#messages-container .message-list");
    if (!messagesContainer) return;
    const messageHtml = message.message_html;
    const isSentByCurrentUser = message.sender_pk == document.body.getAttribute("data-pk");
    const tempDiv = document.createElement('div');
    tempDiv.classList.add("d-flex", "p-1");
    if (isSentByCurrentUser) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        tempDiv.classList.add("flex-row-reverse");
    }
    tempDiv.innerHTML = messageHtml.trim();
    messagesContainer.appendChild(tempDiv);
}

export { establishChatWebSocket, sendChatMessage }
