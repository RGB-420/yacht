export type FeedbackType =
| "wrong_data"
| "missing_data"
| "duplicate"
| "wrong_relation"
| "broken_link"
| "other"
| "regatta_suggestion"

export type FeedbackStatus =
| "pending"
| "reviewed"
| "fixed"
| "ignored"

export type FeedbackBase = {
    entity_type: string
    entity_id?: number
    type: FeedbackType
    message?: string
    page?: string
    link?: string
}

export interface FeedbackCreate extends FeedbackBase {}

export interface Feedback extends FeedbackBase {
    id_feedback: number
    status: FeedbackStatus
    created_at: string
}

export interface FeedbackResponse {
    id_feedback: number
}

export interface UpdateFeedbackStatus {
    status: FeedbackStatus
}