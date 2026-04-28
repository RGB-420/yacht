import { apiFetch } from "../../../shared/api/client"
import type { ScheduleEvent } from "../types"

export const getSchedule = async (): Promise<ScheduleEvent[]> => {
    return apiFetch("/schedule")
}