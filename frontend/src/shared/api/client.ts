const API_URL = import.meta.env.VITE_API_URL

export const apiFetch = async (endpoint: string) => {
    const res = await fetch(`${API_URL}${endpoint}`)

    if (!res.ok) {
        throw new Error("API error")
    }

    return res.json()
}