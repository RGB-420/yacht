import { apiFetch } from "../../../shared/api/client"
import type { ClubRegattas } from "../types"

export const getClubRegattas = (id: string): Promise<ClubRegattas[]> => {
    return apiFetch<ClubRegattas[]>(`/clubs/${id}/regattas`)
}