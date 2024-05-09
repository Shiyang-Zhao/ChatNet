let socket;

const establishNotificationWebSocket = () => {
    if (socket) {
        socket.close();
    }

    const socketProtocol =
        window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketURL =
        socketProtocol + window.location.host + '/ws/notifications/';
    socket = new WebSocket(socketURL);

    socket.onopen = function () {
        console.log("WebSocket connection to notification successfully established!");
    };

    socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log("Received message: " + message.content);
        displayNotificationMessage(message);
    };

    socket.onclose = function (e) {
        console.error(`Chat socket closed unexpectedly: ${e.code} - ${e.reason}`);
    };
};

const displayNotificationMessage = (message) => {
    const notificationContainer = document.querySelector("#notification-list");
    if (notificationContainer) {
        const wrapperDiv = document.createElement("div");
        const notificationElement = document.createElement("li");
        notificationElement.classList.add("list-group-item");
        const messageContent = document.createElement("span");
        messageContent.textContent = message.content;
        notificationElement.appendChild(messageContent);
        wrapperDiv.appendChild(notificationElement);
        notificationContainer.prepend(wrapperDiv);
    } else {
        console.error("Notification container not found.");
    }
};

export { establishNotificationWebSocket };
