import { sendChatMessage } from '../websockets/chat_websocket.js';

const showMessageDetail = (detailPlaceholder) => {
    const messageForm = detailPlaceholder.querySelector('#message-form');
    const messageInput = detailPlaceholder.querySelector('#message-input');
    const sendButton = detailPlaceholder.querySelector('#send-button');
    messageInput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    const sendButtonPopover = new bootstrap.Popover(sendButton, {
        trigger: 'manual',
        html: true,
        content: "You can't send an empty message",
        placement: 'right',
    });

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const messageContent = messageInput.value.trim();
        if (messageContent !== '') {
            sendChatMessage(messageContent);
            messageInput.value = '';
            sendButtonPopover.hide();
        } else {
            sendButtonPopover.show();
            setTimeout(() => { sendButtonPopover.hide(); }, 3000);
        }
    });

    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            const messageContent = messageInput.value.trim();
            if (messageContent !== '') {
                sendChatMessage(messageContent);
                messageInput.value = '';
                sendButtonPopover.hide();
            } else {
                sendButtonPopover.show();
                setTimeout(() => { sendButtonPopover.hide(); }, 3000);
            }
        }
    });
}
export { showMessageDetail }
