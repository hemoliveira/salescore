// In dev, Vite serves the frontend on :5173 and the API runs locally on :8000.
// In production, the API is deployed as a Vercel Function behind the /api
// rewrite on the same origin, so no absolute host is needed.
const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ?? (import.meta.env.DEV ? "http://127.0.0.1:8000" : "");

function apiUrl(path) {
    return `${API_BASE_URL}/api${path}`;
}

// Short-lived GET cache so navigating between pages (or re-rendering) doesn't
// refire identical requests. Any mutation clears it so a follow-up loadData()
// always sees fresh data.
const GET_CACHE_TTL_MS = 15000;
const getCache = new Map();

function getCached(path) {
    const entry = getCache.get(path);
    if (!entry) return null;
    if (Date.now() > entry.expiry) {
        getCache.delete(path);
        return null;
    }
    return entry.promise;
}

function setCached(path, promise) {
    getCache.set(path, { expiry: Date.now() + GET_CACHE_TTL_MS, promise });
    promise.catch(() => getCache.delete(path));
    return promise;
}

export function invalidateCache() {
    getCache.clear();
}

export function apiGet(path) {
    const cached = getCached(path);
    if (cached) return cached;

    const promise = fetch(apiUrl(path)).then(async (response) => {
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || `GET ${path} failed`);
        }
        return response.json();
    });

    return setCached(path, promise);
}

export async function apiPost(path, body) {
    const response = await fetch(apiUrl(path), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `POST ${path} failed`);
    }

    invalidateCache();
    return response.json();
}

export async function apiDelete(path) {
    const response = await fetch(apiUrl(path), {
        method: "DELETE",
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `DELETE ${path} failed`);
    }

    invalidateCache();
    return response.json();
}

export async function apiPut(path, body) {
    const response = await fetch(apiUrl(path), {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `PUT ${path} failed`);
    }

    invalidateCache();
    return response.json();
}