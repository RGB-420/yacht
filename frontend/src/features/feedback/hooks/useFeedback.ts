import { useState } from "react"
import { createFeedback } from "../api/feedbackApi"
import type { FeedbackCreate } from "../types"

export const useFeedback = () => {
    const [loading, setLoading] = useState(false)
    const [success, setSuccess] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const sendFeedback = async (data: FeedbackCreate): Promise<boolean> => {
        setLoading(true)
        setError(null)

        try {
            await createFeedback(data)
            setSuccess(true)
            return true
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to send feedback")
            return false
        } finally {
            setLoading(false)
        }
        }

    const reset = () => {
        setSuccess(false)
        setError(null)
    }

    return  {sendFeedback, loading, success, error, reset }
}