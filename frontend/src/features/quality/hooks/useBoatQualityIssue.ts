import { useEffect, useState } from "react"
import { getBoatQualityIssue } from "../api/qualityApi"
import type { BoatQualityIssueDetail } from "../types"

export const useBoatQualityIssue = (issueKey?: string, page = 1, limit = 50) => {
    const [issue, setIssue] = useState<BoatQualityIssueDetail | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            if (!issueKey) {
                setError("Missing quality issue")
                setLoading(false)
                return
            }

            try {
                setLoading(true)
                setError(null)

                const offset = (page - 1) * limit
                const res = await getBoatQualityIssue(issueKey, limit, offset)
                setIssue(res)
            } catch (err) {
                setError("Error loading quality issue")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [issueKey, page, limit])

    return { issue, loading, error }
}
