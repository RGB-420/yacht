import { useEffect, useState } from "react"
import { getClasses } from "../api/getClasses"
import type { ClassesListItem } from "../types"

export const useClasses = () => {
    const [classes, setClasses] = useState<ClassesListItem[]>([])
    const [loading, setLoading] =useState(true)
    const [error, setError] =useState<string | null>(null)

    useEffect(() => {
        setLoading(true)

        getClasses()
            .then((data) => {
                setClasses(data)
            })
            .catch(() => setError("Error loading classes"))
            .finally(() => setLoading(false))
    }, [])

    return { classes, loading, error }
}