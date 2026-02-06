class PingView {
    constructor() {
        this.socket = null;
    }

    render(container) {
        const template = document.getElementById('view-ping');
        container.innerHTML = '';
        container.appendChild(template.content.cloneNode(true));
        this.startSocket();
    }

    startSocket() {
        this.socket = new WebSocket('ws://127.0.0.1:8000/ws/ping');
        const grid = document.getElementById('ping-grid');
        const statusEl = document.getElementById('connection-status');

        this.socket.onopen = () => {
            statusEl.innerText = "Live Stream Active";
            statusEl.className = "text-sm px-2 py-1 rounded bg-green-100 text-green-800";
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            grid.innerHTML = data.map(item => {
                const isOnline = item.status === 'Online';
                const borderColor = isOnline ? 'border-green-500' : 'border-red-300';
                const bgColor = isOnline ? 'bg-green-50' : 'bg-red-50';
                const textColor = isOnline ? 'text-green-700' : 'text-red-700';
                const icon = isOnline ? '↑' : '↓';

                return `
                <div class="flex flex-col items-center justify-center p-4 bg-white border-b-4 ${borderColor} rounded shadow-sm transition-all hover:shadow-md">
                    <div class="text-lg font-mono font-bold text-gray-700 mb-1">${item.ip}</div>
                    <div class="flex items-center px-3 py-1 rounded-full text-sm font-bold ${bgColor} ${textColor}">
                        <span class="mr-1">${icon}</span> ${item.status}
                    </div>
                </div>
                `;
            }).join('');
        };

        this.socket.onclose = () => {
             if (statusEl) {
                 statusEl.innerText = "Stream Disconnected";
                 statusEl.className = "text-sm px-2 py-1 rounded bg-red-100 text-red-800";
             }
        };
    }

    destroy() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}