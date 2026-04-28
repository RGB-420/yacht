type Props = {
    message: string
    type: "success" | "error"
}

export const FeedbackToast = ({ message, type }: Props) => {
    return (
        <div
            className={`
                fixed bottom-5 right-5 px-4 py-3 rounded-xl shadow-lg z-50
                ${type === "success" ? "bg-green-500 text-textDark" : "bg-red-500 text-textDark"}
                `}
        >
            {message}
        </div>
    )
}