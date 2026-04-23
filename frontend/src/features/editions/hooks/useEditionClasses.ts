import { useEffect, useState } from "react"
import { getEditionClasses } from "../api/getEditionClasses"
import type { EditionClasses } from "../types"

export const useEditionClasses = (id?: string) => {
    const [classes, setClasses] = useState<EditionClasses[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return 

        setLoading(true)

        getEditionClasses(id)
            .then(setClasses)
            .catch(() => setError("Error loading classes"))
            .finally(() => setLoading(false))
    }, [id])

    return { classes, loading, error }
}