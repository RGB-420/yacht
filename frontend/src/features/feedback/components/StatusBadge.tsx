import type { FeedbackStatus } from "../types"

export const StatusBadge = ({ status }: { status: FeedbackStatus}) => {
    const styles = {
        pending: "bg-yellow-100 text-yellow-700",
        reviewed: "bg-blue-100 tex-blue-700",
        fixed: "bg-green-100 text-green-700",
        ignored: "bg-gray-200 text-gray-600"
    }

    return (
        <span className={`px-2 py-1 text-xs rounded-lg ${styles[status]}`}>
            {status}
        </span>
    )
}