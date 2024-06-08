import { sendChatMessage } from '../websockets/chat_websocket.js';

const scrollToLatestMessage = (container) => {
    container.scrollTo({
        top: container.scrollHeight,
    });
};

const sendMessage = (messageInput, sendButtonPopover) => {
    const messageContent = messageInput.value.trim();
    if (messageContent !== '') {
        sendChatMessage(messageContent);
        messageInput.value = '';
        sendButtonPopover.hide();
    } else {
        sendButtonPopover.show();
        setTimeout(() => { sendButtonPopover.hide(); }, 3000);
    }
};

const showMessageDetail = (detailPlaceholder) => {
    if (detailPlaceholder.querySelector("#select-chat-placeholder")) {
        return;
    }
    const messagesContainer = detailPlaceholder.querySelector('.messages-container');
    const messageForm = detailPlaceholder.querySelector('form');
    const messageInput = messageForm.querySelector('textarea');
    const sendButton = messageForm.querySelector('button');
    scrollToLatestMessage(messagesContainer);

    const sendButtonPopover = new bootstrap.Popover(sendButton, {
        trigger: 'manual',
        html: true,
        content: "You can't send an empty message",
        placement: 'right',
    });

    if (messageForm.getAttribute('data-listener-added') === "0") {
        messageForm.addEventListener('submit', (event) => {
            event.preventDefault();
            sendMessage(messageInput, sendButtonPopover);
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
                sendMessage(messageInput, sendButtonPopover);
            }
        });

        messageInput.addEventListener('focus', () => {
            scrollToLatestMessage(messagesContainer);
        });

        messageForm.setAttribute('data-listener-added', "1");
    }
};

export { showMessageDetail };