import { apiFetch } from "../../../shared/api/client"

export const getClassById = async (id: string) => {
    return apiFetch(`/classes/${id}`)
}