import { apiFetch } from "../../../shared/api/client"
import type { BoatEdition } from "../types"

export const getBoatEditions = (id: string): Promise<BoatEdition[]> => {
    return apiFetch(`/boats/${id}/editions`)
}