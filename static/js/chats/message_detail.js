import { sendChatMessage } from '../websockets/chat_websocket.js';

const scrollToLatestMessage = (container) => {
    container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'
    });
};

const sendMessage = (messageInput, sendButtonPopover, messagesContainer) => {
    const messageContent = messageInput.value.trim();
    if (messageContent !== '') {
        sendChatMessage(messageContent);
        messageInput.value = '';
        sendButtonPopover.hide();
        scrollToLatestMessage(messagesContainer);
    } else {
        sendButtonPopover.show();
        setTimeout(() => { sendButtonPopover.hide(); }, 3000);
    }
};

const showMessageDetail = (detailPlaceholder) => {
    const messageForm = detailPlaceholder.querySelector('#message-form');
    const oldMessageInput = detailPlaceholder.querySelector('#message-input');
    const sendButton = detailPlaceholder.querySelector('#send-button');
    const messagesContainer = detailPlaceholder.querySelector('.chat-messages');
    scrollToLatestMessage(messagesContainer);

    const sendButtonPopover = new bootstrap.Popover(sendButton, {
        trigger: 'manual',
        html: true,
        content: "You can't send an empty message",
        placement: 'right',
    });

    // Clone the message input to remove existing event listeners
    const messageInput = oldMessageInput.cloneNode(true);
    oldMessageInput.parentNode.replaceChild(messageInput, oldMessageInput);

    messageInput.addEventListener('input', () => {
        if (messageInput.value.trim() === '') {
            gsap.to(sendButton, { x: 5, width: 0, autoAlpha: 0, duration: 0.2 });
        } else {
            gsap.to(sendButton, { x: 0, width: 'auto', autoAlpha: 1, duration: 0.2 });
        }
    });

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        sendMessage(messageInput, sendButtonPopover, messagesContainer);
    });

    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage(messageInput, sendButtonPopover, messagesContainer);
        }
    });

    messageInput.addEventListener('focus', () => {
        scrollToLatestMessage(messagesContainer);
    });
};

export { showMessageDetail };