const API_BASE_URL = "http://127.0.0.1:8000";

export async function apiGet(path) {
    const response = await fetch(`${API_BASE_URL}${path}`);
    if (!response.ok) {
        throw new Error(`GET ${path} failed with status ${response.status}`);
    }
    return response.json();
}

export async function apiPost(path, body) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
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
    const response = await fetch(`${API_BASE_URL}${path}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `DELETE ${path} failed`);
    }

    return response.json();
}

export async function apiPut(path, body) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
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