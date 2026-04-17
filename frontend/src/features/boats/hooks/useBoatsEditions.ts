import { useEffect, useState } from "react"
import { getBoatEditions } from "../api/getBoatEditions"
import type { BoatEdition } from "../types"

export const useBoatEditions = (id?: string) => {
    const [editions, setEditions] = useState<BoatEdition[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    
    useEffect(() => {
        if (!id) return

        setLoading(true)

        getBoatEditions(id)
            .then(setEditions)
            .catch(() => setError("Error loading participations"))
            .finally(() => setLoading(false))
    }, [id])

    return { editions, loading, error }
}