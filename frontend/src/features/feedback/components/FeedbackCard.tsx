import type { Feedback } from "../types"
import { StatusBadge } from "./StatusBadge"
import { FeedbackActions } from "./FeedbackActions"

import { ExternalLink } from "lucide-react"

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


            {(item.page || item.link) && (
                <div className="mt-3 space-y-2 text-sm">

                    <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                        Links
                    </p>

                    {item.page && (
                        <a
                            href={item.page}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="
                                flex items-center gap-1
                                text-primary dark:text-primaryDark
                                hover:underline
                            "
                        >
                            Page: {item.page}
                            <ExternalLink size={14} />
                        </a>    
                    )}

                    {item.link && (
                        <a
                            href={item.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="
                                flex items-center gap-1
                                text-primary dark:text-primaryDark
                                hover:underline
                            "
                        >
                            Source
                            <ExternalLink size={14} />
                        </a>    
                    )}
                </div>
            )}

            <FeedbackActions
                id={item.id_feedback}
                onChange={onChangeStatus}
            />
        </div>
    )
}