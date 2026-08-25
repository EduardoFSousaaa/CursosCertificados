const Toast = (() => {
    const CATEGORY_MAP = {
        success: { bg: 'bg-success', textClass: 'text-white' },
        danger:  { bg: 'bg-danger',  textClass: 'text-white' },
        error:   { bg: 'bg-danger',  textClass: 'text-white' },
        warning: { bg: 'bg-warning', textClass: 'text-dark'  },
        info:    { bg: 'bg-info',    textClass: 'text-white' },
    };

    function getContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '1090';
            document.body.appendChild(container);
        }
        return container;
    }

    function show(message, category = 'info', delay = 4500) {
        const style = CATEGORY_MAP[category] || CATEGORY_MAP.info;
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center ${style.bg} ${style.textClass} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body fw-semibold">${escapeHtml(message)}</div>
                <button type="button"
                        class="btn-close ${style.textClass === 'text-white' ? 'btn-close-white' : ''} me-2 m-auto"
                        data-bs-dismiss="toast"
                        aria-label="Fechar">
                </button>
            </div>`;

        getContainer().appendChild(toastEl);
        const instance = new bootstrap.Toast(toastEl, { delay });
        instance.show();
        toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    }

    function loadFlashMessages() {
        const el = document.getElementById('__flash__');
        if (!el) return;
        try {
            JSON.parse(el.textContent).forEach(([cat, msg]) => show(msg, cat));
        } catch (_) {}
    }

    return { show, loadFlashMessages };
})();

document.addEventListener('DOMContentLoaded', () => Toast.loadFlashMessages());
