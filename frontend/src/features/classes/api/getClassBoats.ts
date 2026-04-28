import { apiFetch } from "../../../shared/api/client"
import type { BoatClass } from "../types"

export const getClassBoats = (id: string): Promise<BoatClass[]> => {
    return apiFetch<BoatClass[]>(`/classes/${id}/boats`)
}