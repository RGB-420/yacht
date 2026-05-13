import { apiFetch } from "../../../shared/api/client"
import type { FeedbackCreate, FeedbackResponse, Feedback, FeedbackStatus } from "../types"

const getAdminKey = () => localStorage.getItem("admin_code")

export const getFeedback = async (): Promise<Feedback[]> => {
  const key = getAdminKey()

  return apiFetch("/feedback", {
    headers: {
      "x-admin-key": key || ""
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
  const key = getAdminKey()
  
  return apiFetch(`/feedback/${id}`, {
    method: "PATCH", 
    headers: {
      "x-admin-key": key || ""
    },
    body: JSON.stringify({ status })})
} 
