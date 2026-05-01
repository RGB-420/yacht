import type { FeedbackStatus } from "../types"

type Props = {
    id: number
    onChange: (id: number, status: FeedbackStatus) => void
}

export const FeedbackActions = ({ id, onChange }: Props) => {
    return (
        <div className="flex gap-2 pt-2">
            <button
                onClick={() => onChange(id, "fixed")}
                className="px-2 py-1 text-xs bg-green-600 text-white rounded"
            >
                Fix
            </button>

            <button
                onClick={() => onChange(id, "reviewed")}
                className="px-2 py-1 text-xs bg-blue-500 text-white rounded"
            >
                Review
            </button>

            <button
                onClick={() => onChange(id, "ignored")}
                className="px-2 py-1 text-xs bg-gray-500 text-white rounded"
            >
                Ignore
            </button>
        </div>
    )
}