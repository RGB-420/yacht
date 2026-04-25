import { apiFetch } from "../../../shared/api/client"

export const getEditionLinks = async (id: string) => {
    return apiFetch(`/editions/${id}/links`)
}