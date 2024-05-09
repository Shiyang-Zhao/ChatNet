import { establishWebSocket, sendMessage } from "./websocket.js";

const showDetailPlaceholder = (chatPk) => {
    document
        .querySelectorAll(".chat-detail-placeholder")
        .forEach((placeholder) => {
            placeholder.style.display = "none";
        });

    const detailPlaceholder = document.getElementById(
        `chat-detail-placeholder-${chatPk}`
    );
    if (detailPlaceholder) {
        detailPlaceholder.style.display = "block";
        establishWebSocket(chatPk);

        const messageInput = detailPlaceholder.querySelector("#messageInput");
        const sendButton = detailPlaceholder.querySelector("#sendButton");

        sendButton.addEventListener("click", () => {
            if (messageInput.value.trim() !== "") {
                sendMessage({ content: messageInput.value.trim() });
                messageInput.value = "";
            } else {
                alert("You can't send an empty message");
            }
        });

        messageInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                if (messageInput.value.trim() !== "") {
                    // Check if the form is valid
                    sendMessage({ content: messageInput.value.trim() });
                    messageInput.value = "";
                } else {
                    alert("You can't send an empty message");
                }
            }
        });
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const chatPattern = /^\/chats\/chat\/\d+\/$/;
    const currentPath = window.location.pathname;
    if (chatPattern.test(currentPath)) {
        const chatPk = currentPath.match(/\d+/)[0];
        showDetailPlaceholder(chatPk);
    }

    document.querySelectorAll(".list-group-item").forEach((item) => {
        item.addEventListener("click", () => {
            const chatPk = item.getAttribute("data-chat-pk");
            showDetailPlaceholder(chatPk);
            const url = item.getAttribute("data-href");
            window.history.pushState(null, "", url);
        });
    });

    // function toggleSelection(event) {
    //     const option = event.target;
    //     if (option.tagName === 'OPTION') {
    //         option.selected = !option.selected;
    //         if (option.selected) {
    //             option.classList.add('bg-primary');
    //         } else {
    //             option.classList.remove('bg-primary');
    //         }
    //     }
    // }
    // document.getElementById('id_participants').addEventListener('click', toggleSelection);
});
