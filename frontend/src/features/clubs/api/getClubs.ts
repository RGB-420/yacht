import { apiFetch } from "../../../shared/api/client"
import type { ClubsListItem } from "../types"

export const getClubs = (): Promise<ClubsListItem[]> => {
    return apiFetch(`/clubs`)
}