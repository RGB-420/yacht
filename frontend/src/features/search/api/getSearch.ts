import { apiFetch } from "../../../shared/api/client"
import type { SearchResult } from "../types"

export const getSearch = (query: string): Promise<SearchResult> => {
    return apiFetch(`/search?q=${query}`)
}