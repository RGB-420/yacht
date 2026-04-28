import { useEffect, useState } from "react"
import { getSchedule } from "../api/getSchedule"
import type { ScheduleEvent } from "../types"

export const useSchedule = () => {
    const [events, setEvents] = useState<ScheduleEvent[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        getSchedule()
            .then(setEvents)
            .catch(() => setError("Error loading schedule"))
            .finally(() => setLoading(false))
    }, [])

    return { events, loading, error }
}