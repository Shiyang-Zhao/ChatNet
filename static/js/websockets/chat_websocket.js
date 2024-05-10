let socket;
let retryInterval = 1000;
let maxRetryInterval = 60000;

const establishChatWebSocket = (chatPk) => {
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
        var message = JSON.parse(event.data);
        console.log("socket: " + chatPk);
        console.log("Sender: " + message.sender_username);
        console.log("Received message: " + message.content);
        console.log("Date sent: " + message.date_sent);
        displayChatMessage(chatPk, message);
    };

    socket.onclose = function (e) {
        console.error(`Chat socket closed: ${e.code}  ${e.reason}`);
        reconnect(chatPk);
    };

    socket.onerror = function (e) {
        console.error(`WebSocket encountered an error: ${e.code}  ${e.reason}`);
        reconnect(chatPk);
    };
};

const reconnect = (chatPk) => {
    if (socket && socket.chatPk !== chatPk) {
        console.error("WebSocket won't try to reconnect because chat room changed.");
        return;
    }
    console.log(`Attempting to reconnect in ${retryInterval / 1000} seconds...`);
    setTimeout(() => establishChatWebSocket(chatPk), retryInterval);
    retryInterval = Math.min(maxRetryInterval, retryInterval * 2);
};

const sendChatMessage = (content) => {
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

const displayChatMessage = (chatPk, message) => {
    var messagesContainer = document.querySelector(
        `#chat-detail-placeholder-${chatPk} .chat-messages`
    );
    var messageElement = document.createElement("div");
    messageElement.classList.add("message");
    var usernameElement = document.createElement("strong");
    usernameElement.textContent = message.sender_username + ": ";
    messageElement.appendChild(usernameElement);
    var contentElement = document.createElement("span");
    contentElement.textContent = message.content;
    messageElement.appendChild(contentElement);
    var dateSentElement = document.createElement("span");
    dateSentElement.classList.add("date-sent");

    var dateSent = new Date(message.date_sent);
    var options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        hour12: false,
    };
    dateSentElement.textContent = dateSent.toLocaleString("en-US", options);

    messageElement.appendChild(dateSentElement);
    messagesContainer.appendChild(messageElement);
};

export { establishChatWebSocket, sendChatMessage }
