type Tab =
| "all"
| "pending"
| "reviewed"
| "fixed"
| "ignored"
| "suggestions"

type Props = {
    active: Tab
    onChange: (tab: Tab) => void
    counts: Record<Tab, number>
}

export const FeedbackTabs = ({ active, onChange, counts }: Props) => {
    const tabs: Tab[] = [
        "all",
        "pending",
        "reviewed",
        "fixed",
        "ignored",
        "suggestions"
    ]

    return (
        <div className="flex gap-2 flex-wrap
                        bg-background dark:bg-backgroundDark
                        p-2 rounded-xl
                        border border-border dark:border-borderDark
                        w-fit">

            {tabs.map((tab) => {
                const isActive = active === tab

                return (
                    <button
                        key={tab}
                        onClick={() => onChange(tab)}
                        className={`
                            px-3 py-1.5 text-sm rounded-lg
                            transition-all duration-200

                            ${isActive
                                ? "bg-primary text-textDark shadow-md scale-[1-02]"
                                : "text-text dark:text-textDark hover:bg-primary/10 hover:text-primary"
                            }
                        `}
                    >
                        <span className="capitalize">
                            {tab}
                        </span>
                        <span className={`
                            ml-1 text-xs
                            ${isActive ? "text-white/80" : "opacity-60"}
                        `}>
                            ({counts[tab] || 0})    
                        </span>  
                    </button>       
                )
            })}
        </div>
    )
}