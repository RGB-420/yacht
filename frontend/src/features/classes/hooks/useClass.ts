import { useEffect, useState } from "react"
import { getClassById } from "../api/getClassById"
import type { Class } from "../types"

export const useClass = (id?: string) => {
    const [class_, setClass] = useState<Class | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return

        setLoading(true)

        getClassById(id)
            .then(setClass)
            .catch(() => setError("Error loading class"))
            .finally(() => setLoading(false))
    }, [id])

    return { class_, loading, error}
}
