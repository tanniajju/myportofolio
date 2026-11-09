// Helpers shared by the pages that talk to the DRF API (Skill and Experience).

function getCookie(name) {
    const prefix = `${name}=`;
    const cookie = document.cookie.split(';').map(value => value.trim())
        .find(value => value.startsWith(prefix));
    return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
}

function escapeHtml(value) {
    return String(value ?? '').replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;').replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

// Replaces the placeholder UUID in a {% url %} pattern with a real id.
const PLACEHOLDER_UUID = '00000000-0000-0000-0000-000000000000';
function endpointFor(pattern, id) {
    return pattern.replace(PLACEHOLDER_UUID, id);
}

// DRF errors look like {"detail": "..."} (403) or {"field": ["..."]} (400).
function apiErrorMessage(data, status) {
    if (typeof data.detail === 'string') return data.detail;
    const parts = Object.entries(data).map(([field, messages]) => {
        const text = [].concat(messages).filter(m => typeof m === 'string').join(' ');
        return text ? `${field}: ${text}` : '';
    }).filter(Boolean);
    return parts.join(' ') || `Request failed (HTTP ${status}).`;
}

// JSON request that changes data. The CSRF header is required because
// SessionAuthentication enforces CSRF on authenticated writes.
async function apiWrite(url, method, payload) {
    const response = await fetch(url, {
        method,
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: payload === undefined ? undefined : JSON.stringify(payload),
    });
    if (response.status === 204) return null;
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(apiErrorMessage(data, response.status));
    return data;
}