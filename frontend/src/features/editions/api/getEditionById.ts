import { apiFetch } from "../../../shared/api/client"
import type { EditionDetail } from "../types"

export const getEditionById = (id:string): Promise<EditionDetail> => {
    return apiFetch(`/editions/${id}`)
}