import { showMessageDetail } from "./message_detail.js";
import { establishChatWebSocket } from "../../../apps/js/websockets/chat_websocket.js";

function highlightChat(chatContainer) {
    if (!chatContainer) return;
    document.querySelectorAll(".chat-container").forEach(container => {
        container.classList.remove("bg-secondary-subtle");
    });
    if (chatContainer) {
        chatContainer.classList.add("bg-secondary-subtle");
    }
}

function handleChatSelection(url, pk, placeholder) {
    highlightChat(document.querySelector(`#chat-container-${pk}`));
    establishChatWebSocket(pk);
    axios.get(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(response => {
        if (placeholder && response.data.message_html) {
            placeholder.innerHTML = response.data.message_html;
            showMessageDetail(placeholder);
        }
    });
}

function setupChatsContainerEventListener(container, detailPlaceholder) {
    container.addEventListener("click", (event) => {
        const chatContainer = event.target.closest(".chat-container");
        if (chatContainer) {
            const pk = chatContainer.getAttribute("data-pk");
            const url = chatContainer.getAttribute("data-url");
            handleChatSelection(url, pk, detailPlaceholder);
            window.history.pushState(null, "", url);
        }
    });
}

export { handleChatSelection, setupChatsContainerEventListener }