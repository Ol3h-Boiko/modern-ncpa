class Router {
    constructor() {
        this.container = document.getElementById('app-container');
        this.views = {
            'adapters': new AdaptersView(),
            'ping': new PingView()
        };
        this.currentView = null;
    }

    load(viewName) {
        if (this.currentView) {
            this.currentView.destroy();
        }

        document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
        document.getElementById(`btn-${viewName}`).classList.add('active');

        const view = this.views[viewName];
        if (view) {
            view.render(this.container);
            this.currentView = view;
        }
    }
}

const router = new Router();
window.onload = () => router.load('adapters');