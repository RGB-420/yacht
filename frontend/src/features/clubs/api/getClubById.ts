import { apiFetch } from "../../../shared/api/client"
import type { Club } from "../types"

export const getClubById = (id: string): Promise<Club> => {
  return apiFetch<Club>(`/clubs/${id}`)
}