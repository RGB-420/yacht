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

export interface FeedbackCreate {
    entity_type: string
    entity_id?: number
    type: FeedbackType
    message?: string
    page?: string
    link?: string
}

export interface FeedbackResponse {
    id_feedback: number
}