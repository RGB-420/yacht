const API_URL = import.meta.env.VITE_API_URL

export const apiFetch = async <T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> => {

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {})
    }
  })

  if (!res.ok) {
    throw new Error("API error")
  }

  return res.json()
  }
