class AdaptersView {
    constructor() {
        this.root = null;
        this.iconSvg = null;
        this.adaptersData = [];
    }

    async render(container) {
        if (!this.iconSvg) {
            const iconTemplate = document.getElementById('ncpa-icon-template');
            this.iconSvg = iconTemplate ? iconTemplate.innerHTML : '';
        }

        const template = document.getElementById('view-adapters');
        this.root = template.content.cloneNode(true);
        container.innerHTML = '';
        container.appendChild(this.root);
        await this.loadData();
    }

    async loadData() {
        const listContainer = document.getElementById('adapters-list');
        listContainer.innerHTML = '<div class="col-span-full flex justify-center p-8"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>';

        try {
            const response = await fetch('http://127.0.0.1:8000/adapters');
            this.adaptersData = await response.json();

            if (this.adaptersData.length === 0) {
                listContainer.innerHTML = '<div class="col-span-full text-center text-gray-500">No network adapters found.</div>';
                return;
            }

            listContainer.innerHTML = this.adaptersData.map(adapter => {
                const isConnected = adapter.is_connected;
                const statusColor = isConnected ? "text-gray-500" : "text-red-400";
                const iconColor = isConnected ? "text-blue-600" : "text-gray-400";
                const opacityClass = isConnected ? "opacity-100" : "opacity-60 grayscale";
                const bgColor = isConnected ? "hover:bg-blue-50" : "hover:bg-gray-50";

                return `
                <div onclick="router.currentView.openModal('${adapter.id}')"
                     class="flex items-center p-3 bg-white border border-gray-200 rounded shadow-sm ${bgColor} transition cursor-pointer select-none ${opacityClass}">
                    <div class="flex-shrink-0 mr-4">
                        <svg class="h-10 w-10 ${iconColor}" viewBox="0 0 24 24" fill="currentColor">
                            ${this.iconSvg}
                        </svg>
                    </div>

                    <div class="flex-1 min-w-0">
                        <h3 class="text-base font-semibold text-gray-900 leading-tight truncate">
                            ${adapter.friendly_name}
                        </h3>

                        <p class="text-sm ${statusColor} font-medium truncate">
                            ${adapter.status}
                        </p>

                        <p class="text-xs text-gray-400 mt-0.5 truncate border-t border-gray-100 pt-1" title="${adapter.device_name}">
                            ${adapter.device_name}
                        </p>
                    </div>
                </div>
                `;
            }).join('');
        } catch (e) {
            console.error(e);
            listContainer.innerHTML = `<div class="text-red-500">Error: ${e.message}</div>`;
        }
    }

    openModal(adapterId) {
        const adapter = this.adaptersData.find(a => a.id == adapterId);
        if (!adapter) return;

        document.getElementById('m-name').innerText = adapter.friendly_name;
        document.getElementById('m-status').innerText = adapter.status;
        document.getElementById('m-speed').innerText = adapter.speed;
        document.getElementById('m-ipv4').innerText = adapter.details.ipv4;
        document.getElementById('m-ipv6').innerText = adapter.details.ipv6;
        document.getElementById('m-subnet').innerText = adapter.details.subnet;
        document.getElementById('m-gateway').innerText = adapter.details.gateway;
        document.getElementById('m-dns').innerText = adapter.details.dns;
        document.getElementById('m-mac').innerText = adapter.mac;
        document.getElementById('m-driver').innerText = adapter.device_name;

        document.getElementById('details-modal').classList.remove('hidden');
    }

    closeModal() {
        document.getElementById('details-modal').classList.add('hidden');
    }

    destroy() { }
    refresh() { this.loadData(); }
}