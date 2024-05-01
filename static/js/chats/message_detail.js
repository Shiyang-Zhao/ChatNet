document.addEventListener('DOMContentLoaded', function () {
    const chatPk = JSON.parse(document.getElementById('chat-pk').textContent);
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chats/chat/' + chatPk + '/'
    );

    const messagesContainer = document.querySelector('.chat-messages');

    // Connection established
    chatSocket.onopen = function () {
        console.log('WebSocket connection to chat successfully established!');
    };


    chatSocket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log("Sender: " + message.sender_username);
        console.log("Received message: " + message.content);
        console.log("timestamp: " + message.timestamp);
        displayMessage(message);
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.getElementById("sendButton").addEventListener("click", function (event) {
        event.preventDefault();
        sendMessage();
    });

    document.getElementById("message").addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        var messageInput = document.getElementById("message");
        var message = messageInput.value;

        var messageData = {
            'content': message
        };

        chatSocket.send(JSON.stringify(messageData)); // Send the message data as a JSON string
        messageInput.value = ''; // Clear the message input field after sending
    }

    function displayMessage(message) {
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
    }

});