import { useState } from "react"
import { useFeedback } from "../hooks/useFeedback"

type Props = {
    isOpen: boolean
    onClose: () => void
    onSuccess?: () => void
    onError?: () => void
}

export const SuggestRegattaModal = ({ isOpen, onClose, onSuccess, onError }: Props) => {
    const [name, setName] = useState("")
    const [dates, setDates] = useState("")
    const [link, setLink] = useState("")

    const { sendFeedback, loading, reset } = useFeedback()

    if (!isOpen) return null

    const handleSubmit = async () => {
        const ok = await sendFeedback({
            entity_type: "regatta",
            type: "regatta_suggestion",
            message: `Name: ${name}\nDates: ${dates}`,
            link,
            page: window.location.pathname
        })

        if (ok) {
            onSuccess?.()
            handleClose()
        } else {
            onError?.()
        }
    }

    const handleClose = () => {
        onClose()
        reset()
        setName("")
        setDates("")
        setLink("")
    }

    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
            onClick={handleClose}
        >
            <div className="bg-background dark:bg-backgroundDark p-6 rounded-xl w-[400px] space-y-4 shadow-xl"
                onClick={(e) => e.stopPropagation()}
            >

                <h2 className="text-lg font-semibold">
                    Suggest a new regatta
                </h2>

                <input
                    placeholder="Regatta name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="
                        w-full p-2 rounded-lg
                        border-2 border-primary dark:border-primaryDark
                        focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primaryDark
                        text-text dark:text-text"
                />

                <input
                    placeholder="Dates (optional)"
                    value={dates}
                    onChange={(e) => setDates(e.target.value)}
                    className="
                        w-full p-2 rounded-lg
                        border-2 border-primary dark:border-primaryDark
                        focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primaryDark
                        text-text dark:text-text"
                />

                <input
                    placeholder="Link (optional)"
                    value={link}
                    onChange={(e) => setLink(e.target.value)}
                    className="
                        w-full p-2 rounded-lg
                        border-2 border-primary dark:border-primaryDark
                        focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primaryDark
                        text-text dark:text-text"
                />

                <div className="flex justify-end gap-2">
                    <button onClick={handleClose}>
                        Cancel
                    </button>

                    <button
                        onClick={handleSubmit}
                        disabled={loading || !name}
                        className="bg-primary text-white px-4 py-2 rounded-lg"
                    >
                        {loading ? "Sending..." : "Submit"}
                    </button>
                </div>
            </div>
        </div>
    )
}