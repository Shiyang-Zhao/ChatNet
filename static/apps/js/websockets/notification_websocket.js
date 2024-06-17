let socket;
let retryInterval = 1000;
let maxRetryInterval = 60000;

const establishNotificationWebSocket = () => {
    const socketProtocol =
        window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketURL =
        socketProtocol + window.location.host + '/ws/notifications/';
    socket = new WebSocket(socketURL);
    const notificationSound = document.querySelector("#notification-sound");

    socket.onopen = function () {
        console.log("WebSocket connection to notification successfully established!");
        retryInterval = 1000;
    };

    socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log(message)
        displayUnreadNotificationCount(message.unread_count);
        if (message.type === "general_notification") {
            notificationSound.play();
            displayNotificationMessage(message);
        } else if (message.type === "chat_html_notification") {
            displayChatItem(message);
        }
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

function displayChatItem(message) {
    const chatsList = document.querySelector('#chats-container .chat-list');
    if (chatsList && message.chat_html) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = message.chat_html;
        const chatElement = tempDiv.firstElementChild;
        if (chatsList.firstChild) {
            chatsList.insertBefore(chatElement, chatsList.firstChild);
        } else {
            chatsList.appendChild(chatElement);
        }
        gsap.fromTo(chatElement,
            { opacity: 0, y: -20 },
            { duration: 0.5, opacity: 1, y: 0, ease: 'power2.out' }
        );
    }
}

const displayUnreadNotificationCount = (count) => {
    const countElement = document.querySelector("#notification-count");
    if (count > 0) {
        countElement.textContent = count;
        countElement.style.display = 'inline-block';
    } else {
        countElement.textContent = '';
        countElement.style.display = 'none';
    }
};

const displayNotificationMessage = (message) => {
    const notificationContainer = document.querySelector("#notifications-container");
    if (!notificationContainer) return;
    const notificationHtml = message.notification_html;
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = notificationHtml.trim();
    notificationContainer.prepend(tempDiv);
};

export { establishNotificationWebSocket };
