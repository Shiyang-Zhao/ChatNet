let socket;
let retryInterval = 1000;
let maxRetryInterval = 60000;

const establishNotificationWebSocket = () => {
    const socketProtocol =
        window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketURL =
        socketProtocol + window.location.host + '/ws/notifications/';
    socket = new WebSocket(socketURL);
    const soundElement = document.querySelector("#notification-sound");


    socket.onopen = function () {
        console.log("WebSocket connection to notification successfully established!");
        retryInterval = 1000;
    };

    socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log("Message type: " + message.type);
        console.log("Received message: " + message.content);
        console.log("Unread count: " + message.unread_count);
        displayUnreadNotificationCount(message.unread_count);
        if (message.type === "notification_message") {
            soundElement.play();
            displayNotificationMessage(message);
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

const displayUnreadNotificationCount = (count) => {
    const iconElement = document.querySelector("#notification-icon");
    const countElement = document.querySelector("#notification-count");

    if (count > 0) {
        iconElement.classList.add('fa-shake');
        countElement.textContent = count;
        countElement.style.display = 'inline-block';
    } else {
        iconElement.classList.remove("fa-shake");
        countElement.textContent = '';
        countElement.style.display = 'none';
    }
};

const displayNotificationMessage = (message) => {
    const notificationContainer = document.querySelector("#notifications-container");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const markAsReadUrl = `/notifications/notification/${message.notification_pk}/read/`;
    const markAsUnreadUrl = `/notifications/notification/${message.notification_pk}/unread/`;

    if (notificationContainer) {
        const date = new Date(message.date_sent);

        const year = date.getUTCFullYear();
        const month = date.toLocaleString("en-US", { month: "long", timeZone: "UTC" });
        const day = date.getUTCDate();
        let hours = date.getUTCHours();
        const minutes = date.getUTCMinutes().toString().padStart(2, "0");

        if (hours < 10) {
            hours = hours.toString(); // Convert single-digit hours to string without leading zero
        }

        const formattedDate = `${month} ${day}, ${year}, ${hours}:${minutes}`;

        let truncatedContent = message.content.split(" ").slice(0, 50).join(" ");
        if (message.content.split(" ").length > 50) {
            truncatedContent += ' …';
        }

        const notificationHtml = `
            <div class="card mb-2">
                <div class="card-body" style="background-color: #f0f0f0;">
                    <h5 class="card-title"  style="display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; max-height: 7.5em;">
                        ${truncatedContent}
                    </h5>
                    <h6 class="card-subtitle mb-2 text-muted">
                        ${formattedDate.replace(' at', ',')}
                    </h6>
                    <div class="btn-group">
                    <form class="mark-as-read-form me-1" data-url="${markAsReadUrl}">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <button type="submit" class="btn btn-primary me-3">
                            <i class="fas fa-envelope-open-text"></i>
                        </button>
                    </form>
                    <form class="mark-as-unread-form" data-url="${markAsUnreadUrl}">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <button type="submit" class="btn btn-warning">
                            <i class="fas fa-envelope"></i>
                        </button>
                    </form>
                </div>
                </div>
            </div>
        `;
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = notificationHtml.trim();
        notificationContainer.prepend(tempDiv.firstChild);
    }
};

export { establishNotificationWebSocket };
