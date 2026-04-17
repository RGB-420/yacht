import { apiFetch } from "../../../shared/api/client"
import type { BoatDetail } from "../types"

export const getBoatById = (id: string): Promise<BoatDetail> => {
    return apiFetch(`/boats/${id}`)
}