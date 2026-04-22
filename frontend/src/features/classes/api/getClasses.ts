import { apiFetch } from "../../../shared/api/client"
import type { ClassesListItem } from "../../classes/types"

export const getClasses = (): Promise<ClassesListItem[]> => {
    return apiFetch(`/classes`)
}