import { apiFetch } from "../../../shared/api/client"

export const getClubRegattas = async (id: string) => {
    return apiFetch(`/clubs/${id}/regattas`)
}