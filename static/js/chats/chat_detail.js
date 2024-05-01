const chatPattern = /^\/chats\/chat\/\d+\/$/;
let chatSockets = {};
let currentMessageInputs = {};
let currentSendButtons = {};

const connectToChatWebSocket = (chatPk) => {
    if (chatSockets[chatPk]) {
        chatSockets[chatPk].close();
    }

    const wsUrl = `ws://${window.location.host}/ws/chats/chat/${chatPk}/`;
    chatSockets[chatPk] = new WebSocket(wsUrl);

    chatSockets[chatPk].onopen = function () {
        console.log('WebSocket connection to chat successfully established!');
    };

    chatSockets[chatPk].onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log("Sender: " + message.sender_username);
        console.log("Received message: " + message.content);
        console.log("timestamp: " + message.timestamp);
        displayMessage(message, chatPk);
    };

    chatSockets[chatPk].onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
};

const showDetailPlaceholder = (chatPk) => {
    document.querySelectorAll('.chat-detail-placeholder').forEach(placeholder => {
        placeholder.style.display = 'none';
    });

    const detailPlaceholder = document.getElementById(`chat-detail-placeholder-${chatPk}`);
    if (detailPlaceholder) {
        detailPlaceholder.style.display = 'block';
        connectToChatWebSocket(chatPk);

        // Re-select textarea and send button
        currentMessageInputs[chatPk] = detailPlaceholder.querySelector("#message");
        currentSendButtons[chatPk] = detailPlaceholder.querySelector("#sendButton");
    }
};

const sendMessage = (chatPk) => {
    const currentMessageInput = currentMessageInputs[chatPk];
    const currentSendButton = currentSendButtons[chatPk];

    if (!chatSockets[chatPk] || chatSockets[chatPk].readyState !== WebSocket.OPEN) {
        console.error('WebSocket is not open or not connected');
        return;
    }

    var message = currentMessageInput.value.trim(); // Trim whitespace from message

    if (!message) {
        console.error('Message cannot be empty');
        return;
    }

    var messageData = {
        'content': message
    };

    chatSockets[chatPk].send(JSON.stringify(messageData));
    currentMessageInput.value = '';
};

const displayMessage = (message, chatPk) => {
    var messagesContainer = document.querySelector(`#chat-detail-placeholder-${chatPk} .chat-messages`);
    var messageElement = document.createElement("div");
    messageElement.classList.add("message");
    var usernameElement = document.createElement("strong");
    usernameElement.textContent = message.sender_username + ": ";
    messageElement.appendChild(usernameElement);
    var contentElement = document.createElement("span");
    contentElement.textContent = message.content;
    messageElement.appendChild(contentElement);
    var timestampElement = document.createElement("span");
    timestampElement.classList.add("timestamp");
    timestampElement.textContent = message.timestamp;
    messageElement.appendChild(timestampElement);
    messagesContainer.appendChild(messageElement);
};

// Function to close WebSocket connections for chat rooms not matching the current URL pattern
const closeOtherSockets = () => {
    Object.keys(chatSockets).forEach(chatPk => {
        if (!chatPattern.test(window.location.pathname) || !window.location.pathname.includes(chatPk)) {
            chatSockets[chatPk].close();
            delete chatSockets[chatPk];
        }
    });
};

// Check if the current URL matches the chat pattern
const currentPath = window.location.pathname;
if (chatPattern.test(currentPath)) {
    const chatPk = currentPath.match(/\d+/)[0];
    closeOtherSockets(); // Close WebSocket connections for other chat rooms
    showDetailPlaceholder(chatPk);
}

// Set event listener on each chat list item
document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('click', () => {
        const chatPk = item.getAttribute('data-chat-pk');
        closeOtherSockets(); // Close WebSocket connections for other chat rooms
        showDetailPlaceholder(chatPk);
        const url = item.getAttribute("data-href");
        window.history.pushState(null, "", url);
    });
});

// Set event listener for message sending using event delegation
document.addEventListener('click', (event) => {
    Object.keys(currentSendButtons).forEach(chatPk => {
        if (event.target && event.target === currentSendButtons[chatPk]) {
            sendMessage(chatPk);
        }
    });
});

// Set event listener for sending message when Enter key is pressed in message input field
document.addEventListener('keydown', (event) => {
    Object.keys(currentMessageInputs).forEach(chatPk => {
        if (event.key === "Enter" && !event.shiftKey && document.activeElement === currentMessageInputs[chatPk]) {
            event.preventDefault();
            sendMessage(chatPk);
        }
    });
});