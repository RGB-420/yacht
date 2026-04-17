import { useEffect, useState } from "react"
import { getRegattaEditions } from "../api/getRegattaEditions"
import type { EditionListItem } from "../../../features/editions/types"

export const useRegattaEditions = (id?: string) => {
    const [editions, setEditions] = useState<EditionListItem[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return

        setLoading(true)

        getRegattaEditions(id)
            .then(setEditions)
            .catch(() => setError("Error loading editions"))
            .finally(() => setLoading(false))
    }, [id])

    return { editions, loading, error }
}
