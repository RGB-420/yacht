import { apiFetch } from "../../../shared/api/client"
import type { Regatta } from "../types"

export const getRegattaById = (id: string): Promise<Regatta> => {
    return apiFetch<Regatta>(`/regattas/${id}`)
}