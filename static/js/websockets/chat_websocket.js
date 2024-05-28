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
        displayChatMessage(chatPk, message);
    };

    socket.onclose = function (e) {
        console.error(`Chat socket closed: ${e.code}  ${e.reason}`);
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

// const createChat = (chat) => {
//     if (!document.querySelector(`#chat-item-${chatPk}`)) {
//         console.log(`Creating chat: chat_${chatPk}`);
//         const chatList = document.querySelector('#chat-list');
//         chatHtml = ``

//     }
//     console.log(`chat_${chatPk} created`);
// }

const displayChatMessage = (chatPk, message) => {
    let messageHtml = '';
    let messagesContainer = document.querySelector(
        `#chat-detail-placeholder-${chatPk} .chat-messages`
    );
    const profileUrl = `/users/user/${message.sender_username}/profile/detail/`;

    if (!messagesContainer) {

    }

    const loggedInUsername = document.body.getAttribute("data-username");
    const isSentByCurrentUser = message.sender_username === loggedInUsername;
    const formattedDate = new Date(message.date_sent).toLocaleString("en-US", {
        year: "numeric", month: "long", day: "numeric", hour: "numeric", minute: "numeric", hour12: false
    });

    if (isSentByCurrentUser) {
        messageHtml = `
            <div class="message d-flex justify-content-end">
                <div class="text-white p-2" style="max-width: 80%;">
                    <div class="d-flex align-items-start flex-row-reverse">
                        <a href="${profileUrl}" class="text-decoration-none text-reset">
                            <img class="img-fluid rounded-circle ms-2" src="${message.sender_profile_image_url}"
                                style="width: 35px; height: 35px; object-fit: cover;">
                        </a>
                        <div class="d-flex flex-column text-wrap text-break rounded-3 bg-primary ps-2 pe-2" style="max-width: 90%;">
                            <p class="text-start m-1">${message.content}</p>
                            <span class="date-sent text-muted text-start" style="font-size: 0.9em;">
                                ${formattedDate.replace(' at', ',')}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else {
        messageHtml = `
            <div class="message d-flex justify-content-start">
                <div class="text-dark p-2" style="max-width: 80%;">
                    <div class="d-flex align-items-start">
                        <a href="${profileUrl}" class="text-decoration-none text-reset">
                            <img class="img-fluid rounded-circle me-2" src="${message.sender_profile_image_url}"
                                style="width: 35px; height: 35px; object-fit: cover;">
                        </a>
                        <div class="d-flex flex-column text-wrap text-break rounded-3 bg-secondary-subtle ps-2 pe-2" style="max-width: 90%;">
                            <p class="text-start m-1">${message.content}</p>
                            <span class="date-sent text-muted text-end" style="font-size: 0.9em;">
                                ${formattedDate.replace(' at', ',')}
                            </span>
                        </div>
                    </div>
                    
                </div>
            </div>
        `;
    }

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = messageHtml.trim();
    const messageElement = tempDiv.firstChild;
    messagesContainer.appendChild(messageElement);

    if (isSentByCurrentUser) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
};

export { establishChatWebSocket, sendChatMessage }
