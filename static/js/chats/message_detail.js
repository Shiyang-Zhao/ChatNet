document.addEventListener('DOMContentLoaded', function () {
    const chatPk = JSON.parse(document.getElementById('chat-pk').textContent);
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chats/chat/' + chatPk + '/'
    );

    const messageInput = document.querySelector('#messageInput');
    const messagesContainer = document.querySelector('.chat-messages');

    // Connection established
    chatSocket.onopen = function () {
        console.log('WebSocket connection to chat successfully established!');
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        appendMessage(data.sender, data.message, data.timestamp);
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#messageForm').onsubmit = function (e) {
        e.preventDefault();
        const message = messageInput.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        appendMessage('You', message, new Date().toLocaleTimeString());  // Adjust the timestamp format as needed
        messageInput.value = '';
    };

    messageInput.onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            e.preventDefault(); // Avoid form submit on enter key
            document.querySelector('.btn').click(); // Simulate button click
        }
    };

    // Helper function to append messages to the DOM
    function appendMessage(sender, message, timestamp) {
        const newMessage = document.createElement('div');
        newMessage.className = 'message';
        newMessage.innerHTML = `<p><strong>${sender}:</strong> ${message}</p>
                                <span class="timestamp">${timestamp}</span>`;
        messagesContainer.appendChild(newMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;  // Scroll to the latest message
    }
});
