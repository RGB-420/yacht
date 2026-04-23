import { apiFetch } from "../../../shared/api/client"

export const getClassBoats = async (id: string) => {
    return apiFetch(`/classes/${id}/boats`)
}