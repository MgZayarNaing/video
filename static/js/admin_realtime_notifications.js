// static/js/admin_realtime_notifications.js

document.addEventListener('DOMContentLoaded', function() {
    var socket = new WebSocket('ws://' + window.location.host + '/ws/notifications/');

    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var notificationsElement = document.getElementById('notifications');
        if (notificationsElement) {
            var notification = document.createElement('div');
            notification.innerText = data.message;
            notificationsElement.appendChild(notification);
        }
    };

    socket.onclose = function(e) {
        console.error('WebSocket closed unexpectedly');
    };
});
