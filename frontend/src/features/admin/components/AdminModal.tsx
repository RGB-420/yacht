type Props = {
    open: boolean
    code: string
    error: boolean
    onClose: () => void
    onChange: (value: string) => void
    onSubmit: () => void
}

export const AdminModal = ({ open, code, error, onClose, onChange, onSubmit }: Props) => {
    if (!open) return null

    return (
        <div
            className="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
            onClick={onClose}
        >
            <div
                className="
                    bg-background dark:bg-backgroundDark
                    p-6 rounded-xl
                    space-y-4
                    w-[300px]
                    shadow-xl    
                "
                onClick={(e) => e.stopPropagation()}
            >
                <h2 className="text-lg font-semibold">
                    Admin Access
                </h2>

                <input
                    type="password"
                    value={code}
                    autoFocus
                    onChange={(e) => {
                        onChange(e.target.value)
                    
                        if (error) onChange(e.target.value)
                    }}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            onSubmit()
                        }
                    }}
                    placeholder="Enter code"
                    className="
                        w-full p-2 rounded-lg text-text
                        border border-primary dark:border-primaryDark
                        focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primaryDark
                    "
                />

                {error && (
                    <p className="text-red-500 text-sm font-medium">
                        Incorrect code
                    </p>
                )}

                <button
                    onClick={onSubmit}
                    className="
                        w-full
                        bg-primary text-white
                        py-2 rounded-lg
                        hover:bg-primaryDark
                    "
                >
                    Enter
                </button>
            </div>
        </div>
    )
}