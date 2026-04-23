import { apiFetch } from "../../../shared/api/client"

export const getClubById = async (id: string) => {
    return apiFetch(`/clubs/${id}`)
}