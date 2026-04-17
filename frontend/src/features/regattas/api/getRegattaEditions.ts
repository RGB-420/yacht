import { apiFetch } from "../../../shared/api/client"
import type { EditionListItem } from "../../editions/types"

export const getRegattaEditions = (id: string): Promise<EditionListItem[]> => {
    return apiFetch(`/regattas/${id}/editions`)
}