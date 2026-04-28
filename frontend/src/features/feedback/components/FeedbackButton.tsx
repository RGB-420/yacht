import { useState } from "react"
import { FeedbackModal } from "./FeedbackModal"
import { FeedbackToast } from "./FeedbackToast"
import { AlertCircle } from "lucide-react"

type Props = {
    entityType: string
    entityId?: number
    label?: string
}

export const FeedbackButton = ({entityType, entityId}: Props) => {
    const [open, setOpen] = useState(false)
    const [toast, setToast] = useState<{
        message: string
        type: "success" | "error"
    } | null>(null)


    return (
        <>
            <button
                onClick={() => setOpen(true)}
                className="
                    inline-flex items-center gap-2 px-3 py-2
                    border-2 border-border dark:border-borderDark rounded-xl
                    text-text dark:text-textDark
                    hover:text-textDark dark:hover:text-white
                    hover:border-primary hover:bg-primary/10
                    transition-colors
                "
                title="Report issue"
            >
                {/* Icono siempre */}
                <AlertCircle size={18}   className="text-text dark:text-textDark"
  />

                {/* Texto solo en desktop */}
                <span className="hidden sm:inline">
                    Report issue
                </span>
            </button> 

            <FeedbackModal
                isOpen={open}
                onClose={() => setOpen(false)}
                entityType={entityType}
                entityId={entityId}
                onSuccess={() => {
                    setToast({ message: "Thanks! Feedback sent", type: "success" })
                    setTimeout(() => setToast(null), 3000)
                }}
                onError={() => {
                    setToast({message: "Error sendign feedback", type: "error"})
                    setTimeout(() => setToast(null), 3000)
                }}
            />  

            {toast && (
                <FeedbackToast message={toast.message} type={toast.type} />
            )}
        </>
    )
}