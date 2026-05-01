import { useState } from "react"
import { SuggestRegattaModal } from "./SuggestRegattaModal"
import { FeedbackToast } from "./FeedbackToast"
import { CalendarPlus } from "lucide-react"

export const SuggestRegattaButton = () => {
    const [open, setOpen] = useState(false)
    const [toast, setToast] =useState<{
        message: string
        type: "success" | "error"
    } | null>(null)

    return (
        <>
            <button
                onClick={() => setOpen(true)}
                className="inline-flex items-center gap-2 px-3 py-2 border-2 border-border dark:border-borderDark rounded-xl text-text dark:text-textDark hover:bg-primary dark:hover:bg-primaryDark hover:text-white transition-colors"
                title="Suggest Regatta"
            >
                {/* Icono siempre */}
                <CalendarPlus size={18}   className="text-text dark:text-textDark"
            />

                {/* Texto solo en desktop */}
                <span className="hidden sm:inline">
                    Suggest regatta
                </span>
            </button> 

            <SuggestRegattaModal
                isOpen={open}
                onClose={() => setOpen(false)}
                onSuccess={() => {
                    setToast({ message: "Thanks! Suggestion sent", type: "success" })
                    setTimeout(() => setToast(null), 3000)
                }}
                onError={() => {
                    setToast({ message: "Error sending suggestion", type: "error" })
                    setTimeout(() => setToast(null), 3000)
                }}
            />

            {toast && (
                <FeedbackToast message={toast.message} type={toast.type} />
            )}
        </>
    )
}