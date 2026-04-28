import { apiFetch } from "../../../shared/api/client"
import type { EditionLink } from "../types"

export const getEditionLinks = (id: string): Promise<EditionLink[]> => {
    return apiFetch<EditionLink[]>(`/editions/${id}/links`)
}