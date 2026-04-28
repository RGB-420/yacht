import { apiFetch } from "../../../shared/api/client"
import type { FeedbackCreate, FeedbackResponse } from "../types"

export const createFeedback = async (
  data: FeedbackCreate
): Promise<FeedbackResponse> => {

  return apiFetch<FeedbackResponse>("/feedback", {
    method: "POST",
    body: JSON.stringify(data)
  })
}