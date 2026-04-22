import { useEffect, useState } from "react"
import { getClubs } from "../api/getClubs"
import type { ClubsListItem } from "../types"

export const useClubs = () => {
    const [clubs, setClubs] = useState<ClubsListItem[]>([])
    const [loading, setLoading] =useState(true)
    const [error, setError] =useState<string | null>(null)

    useEffect(() => {
        setLoading(true)

        getClubs()
            .then((data) => {
                setClubs(data)
            })
            .catch(() => setError("Error loading clubs"))
            .finally(() => setLoading(false))
    }, [])

    return { clubs, loading, error }
}