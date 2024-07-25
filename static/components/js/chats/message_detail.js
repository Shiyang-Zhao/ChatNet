import { sendChatMessage } from '../../../apps/js/websockets/chat_websocket.js';
import { scrollToLatestMessage } from '../../../apps/js/base/base.js';

const sendMessage = (pk, messageInput, sendButtonPopover) => {
    const messageContent = messageInput.value.trim();
    if (messageContent !== '') {
        sendChatMessage(pk, messageContent);
        messageInput.value = '';
        sendButtonPopover.hide();
    } else {
        sendButtonPopover.show();
        setTimeout(() => { sendButtonPopover.hide(); }, 3000);
    }
};

const showMessageDetail = (pk, container) => {
    const messagesContainer = container.querySelector('.message-list');
    const messageFormContainer = container.querySelector('.message-form-container');
    const messageForm = messageFormContainer.querySelector('form');
    const messageInput = messageFormContainer.querySelector('textarea');
    const sendButton = messageFormContainer.querySelector('button');
    scrollToLatestMessage(messagesContainer);

    const sendButtonPopover = new bootstrap.Popover(sendButton, {
        trigger: 'manual',
        html: true,
        content: "You can't send an empty message",
        placement: 'right',
    });

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        sendMessage(pk, messageInput, sendButtonPopover);
    });

    messageInput.addEventListener('input', () => {
        if (messageInput.value.trim() === '') {
            gsap.to(sendButton, { x: 5, width: 0, autoAlpha: 0, duration: 0.2 });
        } else {
            gsap.to(sendButton, { x: 0, width: 'auto', autoAlpha: 1, duration: 0.2 });
        }
    });

    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage(pk, messageInput, sendButtonPopover);
        }
    });

    messageInput.addEventListener('focus', () => {
        scrollToLatestMessage(messagesContainer);
    });
};

export { showMessageDetail };