const BASE_URL = 'http://localhost:8000'

export async function runAutopsy(idea) {
    const response = await fetch(`${BASE_URL}/autopsy`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail?.error || errorData.detail || 'Failed to perform autopsy');
    }

    return response.json();
}

export async function searchGraveyard(query) {
    const response = await fetch(`${BASE_URL}/graveyard/search?query=${encodeURIComponent(query)}`);

    if (!response.ok) {
        throw new Error('Failed to search graveyard');
    }

    return response.json();
}

export async function getHealth() {
    const response = await fetch(`${BASE_URL}/health`);

    if (!response.ok) {
        throw new Error('System offline');
    }

    return response.json();
}
