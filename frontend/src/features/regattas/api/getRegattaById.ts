import { apiFetch } from "../../../shared/api/client"

export const getRegattaById = async (id: string) => {
    return apiFetch(`/regattas/${id}`)
}