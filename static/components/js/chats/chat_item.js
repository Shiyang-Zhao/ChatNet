import { showMessageDetail } from "./message_detail.js";

function highlightChat(targetContainer) {
    if (!targetContainer) return;
    document.querySelectorAll(".chat-container").forEach(container => {
        container.classList.remove("bg-secondary-subtle");
    });
    targetContainer.classList.add("bg-secondary-subtle");
}

function handleChatSelection(url, pk, container) {
    highlightChat(document.querySelector(`#chat-container-${pk}`));
    axios.get(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(response => {
        if (container && response.data.message_html) {
            container.innerHTML = response.data.message_html;
            showMessageDetail(pk, container);
        }
    });
}

function setChatsContainerEventListener(chatsContainer, messagesContainer) {
    chatsContainer.addEventListener("click", (event) => {
        const chatContainer = event.target.closest(".chat-container");
        if (chatContainer) {
            const pk = chatContainer.getAttribute("data-pk");
            const url = chatContainer.getAttribute("data-url");
            handleChatSelection(url, pk, messagesContainer);
            window.history.pushState(null, "", url);
        }
    });
}

export { handleChatSelection, setChatsContainerEventListener }