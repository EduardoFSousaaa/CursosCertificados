const Http = {
    async get(url) {
        const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        if (!res.ok) throw new Error(`GET ${url} → ${res.status}`);
        return res.text();
    },

    async post(url, data = {}, csrfToken = null) {
        const headers = { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' };
        if (csrfToken) headers['X-CSRFToken'] = csrfToken;
        const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(data) });
        if (!res.ok) throw new Error(`POST ${url} → ${res.status}`);
        return res.json();
    },
};
