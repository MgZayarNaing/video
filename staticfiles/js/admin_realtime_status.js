// static/js/admin_realtime_status.js

document.addEventListener('DOMContentLoaded', function() {
    var socket = new WebSocket('ws://' + window.location.host + '/ws/status/');

    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var statusElement = document.getElementById('user-status');
        if (statusElement) {
            statusElement.innerText = data.message;
        }
    };

    socket.onclose = function(e) {
        console.error('WebSocket closed unexpectedly');
    };
});
