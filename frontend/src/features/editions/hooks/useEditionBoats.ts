import { useEffect, useState } from "react"
import { getEditionBoats } from "../api/getEditionBoats"
import type { BoatListItem } from "../../boats/types"

export const useEditionBoats = (id?: string) => {
    const [boats, setBoats] = useState<BoatListItem[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return 

        setLoading(true)

        getEditionBoats(id)
            .then(setBoats)
            .catch(() => setError("Error loading boats"))
            .finally(() => setLoading(false))
    }, [id])

    return { boats, loading, error }
}