import { apiFetch } from "../../../shared/api/client"

export const getEditionClasses = async (id: string) => {
    return apiFetch(`/editions/${id}/classes`)
}