import { apiFetch } from "../../../shared/api/client"
import type { ClubBoats } from "../types"

export const getClubBoats = (id: string): Promise<ClubBoats[]> => {
    return apiFetch<ClubBoats[]>(`/clubs/${id}/boats`)
}