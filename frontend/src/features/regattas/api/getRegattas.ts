import { apiFetch } from "../../../shared/api/client"
import type { PaginatedRegattas } from "../types"

export const getRegattas = (
    page: number,
    limit: number
): Promise<PaginatedRegattas> => {
    const offset = (page - 1) * limit

    return apiFetch(`/regattas?limit=${limit}&offset=${offset}`)
}