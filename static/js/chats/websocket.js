let socket;

export const establishWebSocket = (chatPk) => {
    if (socket) {
        socket.close();
    }

    const socketProtocol =
        window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketURL =
        socketProtocol + window.location.host + `/ws/chats/chat/${chatPk}/`;
    socket = new WebSocket(socketURL);

    socket.onopen = function () {
        console.log("WebSocket connection to chat successfully established!");
    };

    socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log("socket: " + chatPk);
        console.log("Sender: " + message.sender_username);
        console.log("Received message: " + message.content);
        console.log("Date sent: " + message.date_sent);
        displayMessage(chatPk, message);
    };

    socket.onclose = function (e) {
        console.error("Chat socket closed unexpectedly");
    };
};

export const sendMessage = (messageData) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.error("WebSocket is not open or not connected");
        return;
    }

    socket.send(JSON.stringify(messageData));
};

const displayMessage = (chatPk, message) => {
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

export default socket;
