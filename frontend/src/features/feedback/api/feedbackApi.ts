import { apiFetch } from "../../../shared/api/client"
import type { FeedbackCreate, FeedbackResponse, Feedback, FeedbackStatus } from "../types"

const ADMIN_KEY = import.meta.env.VITE_ADMIN_KEY

export const getFeedback = async (): Promise<Feedback[]> => {
  return apiFetch("/feedback", {
    headers: {
      "x-admin-key": ADMIN_KEY
    }
  })
}

export const createFeedback = async (
  data: FeedbackCreate
): Promise<FeedbackResponse> => {

  return apiFetch<FeedbackResponse>("/feedback", {
    method: "POST",
    body: JSON.stringify(data)
  })
}

export const updateFeedbackStatus = async (id: number, status: FeedbackStatus) => {
  return apiFetch(`/feedback/${id}`, {
    method: "PATCH", 
    headers: {
      "x-admin-key": ADMIN_KEY
    },
    body: JSON.stringify({ status })})
} 
