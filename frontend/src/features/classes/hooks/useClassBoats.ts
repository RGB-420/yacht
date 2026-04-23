import { useEffect, useState } from "react"
import { getClassBoats } from "../api/getClassBoats"
import type { BoatClass } from "../types"

export const useClassBoat = (id?: string) => {
    const [boats, setBoats] = useState<BoatClass[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    
    useEffect(() => {
        if (!id) return

        setLoading(true)

        getClassBoats(id)
            .then(setBoats)
            .catch(() => setError("Error loading boats"))
            .finally(() => setLoading(false))
    }, [id])

    return { boats, loading, error }
}