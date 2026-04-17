import { apiFetch } from "../../../shared/api/client"
import type { BoatListItem } from "../../boats/types"

export const getEditionBoats = (id: string): Promise<BoatListItem[]> => {
    return apiFetch(`/editions/${id}/boats`)
}