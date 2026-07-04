// In dev, Vite serves the frontend on :5173 and the API runs locally on :8000.
// In production, the API is deployed as a Vercel Function behind the /api
// rewrite on the same origin, so no absolute host is needed.
const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ?? (import.meta.env.DEV ? "http://127.0.0.1:8000" : "");

function apiUrl(path) {
    return `${API_BASE_URL}/api${path}`;
}

export async function apiGet(path) {
    const response = await fetch(apiUrl(path));
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `GET ${path} failed`);
    }
    return response.json();
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

    return response.json();
}