let socket;
let retryInterval = 1000;
let maxRetryInterval = 60000;

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
        retryInterval = 1000;
    };

    socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log("Received message: " + message.content);
        displayNotificationMessage(message);
    };

    socket.onclose = function (e) {
        console.error(`Chat socket closed unexpectedly: ${e.code} ${e.reason}`);
        reconnect();
    };

    socket.onerror = function (e) {
        console.error(`WebSocket encountered an error: ${e.code} ${e.reason}`);
        reconnect();
    };
};

const reconnect = () => {
    console.log(`Attempting to reconnect in ${retryInterval / 1000} seconds...`);
    setTimeout(establishNotificationWebSocket, retryInterval);
    retryInterval = Math.min(maxRetryInterval, retryInterval * 2);
};

const displayNotificationMessage = (message) => {
    const notificationContainer = document.querySelector("#notification-list");
    const wrapperDiv = document.createElement("div");
    const notificationElement = document.createElement("li");
    notificationElement.classList.add("list-group-item");
    const messageContent = document.createElement("span");
    messageContent.textContent = message.content;
    notificationElement.appendChild(messageContent);
    wrapperDiv.appendChild(notificationElement);
    notificationContainer.prepend(wrapperDiv);
};

export { establishNotificationWebSocket };
