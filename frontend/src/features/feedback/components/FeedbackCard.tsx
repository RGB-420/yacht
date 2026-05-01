import type { Feedback } from "../types"
import { StatusBadge } from "./StatusBadge"
import { FeedbackActions } from "./FeedbackActions"

type Props = {
    item: Feedback
    onChangeStatus: (id:number, status: Feedback["status"]) => void
}

export const FeedbackCard = ({ item, onChangeStatus }: Props) => {
    return (
        <div
            className="
                p-4 rounded-xl
                border border-border dark:border-borderDark
                bg-background dark:bg-backgroundDark
                space-y-2"
        >
            <div className="flex justify-between items-center">
                <div className="font-semibold">
                    {item.type} · {item.entity_type}
                </div>

                <StatusBadge status={item.status} />
            </div>

            {item.message && (
                <div className="text-sm opacity-80 whitespace-pre-line">
                    {item.message}
                </div>
            )}

            {item.link && (
                <a
                    href={item.link}
                    target="_blank"
                    className="text-primary text-sm hover:underline"
                >
                    Open link
                </a>
            )}

            {item.page && (
                <div className="text-xs opacity-60">
                    {item.page}
                </div>
            )}

            <FeedbackActions
                id={item.id_feedback}
                onChange={onChangeStatus}
            />
        </div>
    )
}