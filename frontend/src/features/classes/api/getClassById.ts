import { apiFetch } from "../../../shared/api/client"
import type { Class } from "../types"    

export const getClassById = (id: string): Promise<Class> => {
    return apiFetch<Class>(`/classes/${id}`)
}