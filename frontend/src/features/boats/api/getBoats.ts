import { apiFetch } from "../../../shared/api/client"
import type { PaginatedBoats } from "../types"

export const getBoats = (
    page: number,
    limit:number
): Promise<PaginatedBoats> => {

    const offset = (page - 1) * limit

    return apiFetch(`/boats?limit=${limit}&offset=${offset}`)
}