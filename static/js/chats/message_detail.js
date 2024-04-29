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
        const newMessage = document.createElement('div');
        newMessage.className = 'message';
        newMessage.innerHTML = `<p><strong>${data.sender}:</strong> ${data.message}</p>
                                <span class="timestamp">${data.timestamp}</span>`;
        messagesContainer.appendChild(newMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
        messageInput.value = '';
    };

    messageInput.onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            e.preventDefault(); // Avoid form submit on enter key
            document.querySelector('.btn').click(); // Simulate button click
        }
    };
});
