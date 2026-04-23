import { useEffect, useState } from "react"
import { getClubBoats } from "../api/getClubBoats"
import type { ClubBoats } from "../types"

export const useClubBoats = (id?: string) => {
    const [boats, setBoats] = useState<ClubBoats[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    
    useEffect(() => {
        if (!id) return

        setLoading(true)

        getClubBoats(id)
            .then(setBoats)
            .catch(() => setError("Error loading boats"))
            .finally(() => setLoading(false))
    }, [id])

    return { boats, loading, error }
}