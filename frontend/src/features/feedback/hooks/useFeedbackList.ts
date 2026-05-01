import { useEffect, useState } from "react"
import { getFeedback, updateFeedbackStatus } from "../api/feedbackApi"
import type { Feedback, FeedbackStatus } from "../types"

export const useFeedbackList = () => {
    const [data, setData] = useState<Feedback[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await getFeedback()
                setData(res)
            } catch (err) {
                setError("Error loading feedback")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    const changeStatus = async (id: number, status: FeedbackStatus) => {
        const previous = data

        try {
            setData((prev) =>
                prev.map((f) =>
                    f.id_feedback === id ? {...f, status } : f
                )
            )

            await updateFeedbackStatus(id, status)
        } catch (err) {
            setData(previous)
            setError("Error updating status")
        }
    }

    return { data, loading, error, changeStatus }
}