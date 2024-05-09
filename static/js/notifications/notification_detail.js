import { establishNotificationWebSocket } from "../websockets/notification_websocket.js";

document.addEventListener("DOMContentLoaded", () => {
    establishNotificationWebSocket();
});