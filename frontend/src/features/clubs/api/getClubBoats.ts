import { apiFetch } from "../../../shared/api/client"

export const getClubBoats = async (id: string) => {
    return apiFetch(`/clubs/${id}/boats`)
}