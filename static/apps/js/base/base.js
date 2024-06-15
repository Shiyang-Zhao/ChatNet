import { establishNotificationWebSocket } from "../websockets/notification_websocket.js";
import { establishChatWebSocket } from "../websockets/chat_websocket.js";
document.addEventListener("DOMContentLoaded", () => {
    establishNotificationWebSocket();
    establishChatWebSocket();
});

const scrollToLatestMessage = (container) => {
    container.scrollTo({
        top: container.scrollHeight,
    });
};

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
export { getCookie, scrollToLatestMessage }