import { useEffect, useState } from "react"
import { getClubById } from "../api/getClubById"
import type { Club } from "../types"

export const useClub = (id?: string) => {
    const [club, setClub] = useState<Club | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return

        setLoading(true)

        getClubById(id)
            .then(setClub)
            .catch(() => setError("Error loading club"))
            .finally(() => setLoading(false))
    }, [id])

    return { club, loading, error}
}
