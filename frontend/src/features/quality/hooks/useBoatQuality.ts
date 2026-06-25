import { useEffect, useState } from "react"
import { getBoatQualityIssues, getBoatQualityMetrics } from "../api/qualityApi"
import type { BoatQualityIssues, BoatQualityMetrics } from "../types"

export const useBoatQuality = () => {
    const [metrics, setMetrics] = useState<BoatQualityMetrics | null>(null)
    const [issues, setIssues] = useState<BoatQualityIssues | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [metricsRes, issuesRes] = await Promise.all([
                    getBoatQualityMetrics(),
                    getBoatQualityIssues(10)
                ])

                setMetrics(metricsRes)
                setIssues(issuesRes)
            } catch (err) {
                setError("Error loading quality metrics")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    return { metrics, issues, loading, error }
}
