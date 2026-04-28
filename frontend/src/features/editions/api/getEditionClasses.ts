import { apiFetch } from "../../../shared/api/client"
import type { EditionClasses } from "../types"

export const getEditionClasses = (id: string): Promise<EditionClasses[]> => {
    return apiFetch<EditionClasses[]>(`/editions/${id}/classes`)
}