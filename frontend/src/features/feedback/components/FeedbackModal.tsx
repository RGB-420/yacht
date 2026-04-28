import { useState } from "react"
import { useFeedback } from "../hooks/useFeedback"
import type { FeedbackType } from "../types"

type Props = {
    isOpen: boolean
    onClose: () => void
    entityType: string
    entityId?: number
    onSuccess?: () => void
    onError?: () => void
}

export const FeedbackModal = ({isOpen, onClose, entityType, entityId, onSuccess, onError}: Props) => {
    const [type, setType] = useState<FeedbackType>("wrong_data")
    const [message, setMessage] = useState("")

    const { sendFeedback, loading, reset } = useFeedback()

    if (!isOpen) return null

    const handleSubmit = async () => {
        const ok = await sendFeedback({
            entity_type: entityType,
            entity_id: entityId,
            type,
            message,
            page: window.location.pathname
        })

        if (ok) {
            onSuccess?.()
            onClose()
        } else {
            onError?.()
        }
        }

    const handleClose = () => {
        onClose()
        reset()
        setMessage("")
        setType("wrong_data")
    }

    return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
        onClick={handleClose}
    >
        <div className="bg-background dark:bg-backgroundDark p-6 rounded-xl w-[400px] space-y-4 shadow-xl"
            onClick={(e) => e.stopPropagation()}>

            <h2 className="text-lg font-semibold">
            Report an issue
            </h2>

            {/* Tipo de error */}
            <select
                value={type}
                onChange={(e) => setType(e.target.value as FeedbackType)}
                className="
                    w-full p-2 rounded-lg
                    border-2 border-primary dark:border-primaryDark
                    focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primaryDark
                    text-text dark:text-text"
                >
                <option value="wrong_data">Wrong data</option>
                <option value="missing_data">Missing data</option>
                <option value="duplicate">Duplicate</option>
                <option value="wrong_relation">Wrong relation</option>
                <option value="broken_link">Broken link</option>
                <option value="other">Other</option>
            </select>

            {/* Mensaje */}
            <textarea
                placeholder="Describe the issue (optional)"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="
                w-full p-2 h-24 rounded-lg
                border-2 border-primary dark:border-primaryDark
                focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primaryDark
                text-text dark:text-text"
            />

            {/* Botones */}
            <div className="flex justify-end gap-2">
            <button
                onClick={handleClose}
                className="px-3 py-2"
            >
                Cancel
            </button>

            <button
                onClick={handleSubmit}
                disabled={loading}
                className="bg-primary dark:bg-primaryDark text-textDark px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
            >
                {loading ? "Sending..." : "Submit"}
            </button>
            </div>
        </div>
    </div>
    )
}