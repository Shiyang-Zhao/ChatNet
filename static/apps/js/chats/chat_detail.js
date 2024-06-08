import { establishChatWebSocket } from "../websockets/chat_websocket.js";
import { showMessageDetail } from "../../../components/js/chats/message_item.js";

document.addEventListener("DOMContentLoaded", function () {
    const chatsContainer = document.querySelector('#chats-container');
    const chatDetailPlaceholder = document.querySelector('#message-detail-placeholder');

    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (chatPattern.test(currentPath)) {
        const pk = currentPath.match(/\d+/)[0];
        const chatContainer = document.querySelector(`#chat-container-${pk}`);
        if (chatContainer) {
            highlightChat(chatContainer);
        }
        axios.get(currentPath, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => {
            if (chatDetailPlaceholder && response.data.message_html) {
                chatDetailPlaceholder.innerHTML = response.data.message_html;
                showMessageDetail(chatDetailPlaceholder);
            }
        });
        establishChatWebSocket(pk);
    }

    if (chatsContainer) {
        chatsContainer.addEventListener("click", (event) => {
            const chatContainer = event.target.closest(".chat-container");
            if (chatContainer) {
                const pk = chatContainer.getAttribute("data-pk");
                const url = chatContainer.getAttribute("data-url");
                highlightChat(chatContainer);
                establishChatWebSocket(pk);
                axios.get(url, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                }).then(response => {
                    if (chatDetailPlaceholder && response.data.message_html) {
                        chatDetailPlaceholder.innerHTML = response.data.message_html;
                        showMessageDetail(chatDetailPlaceholder);
                    }
                });
                window.history.pushState(null, "", url);
            }
        });
    }

    function highlightChat(chatContainer) {
        if (!chatContainer) return;
        document.querySelectorAll(".chat-container").forEach(container => {
            container.classList.remove("bg-secondary-subtle");
        });
        if (chatContainer) {
            chatContainer.classList.add("bg-secondary-subtle");
        }
    }
});
