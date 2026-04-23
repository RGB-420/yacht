import { useState } from "react"
import { ChevronDown, ChevronRight } from "lucide-react"

interface Props {
  title: string
  count?: number
  defaultOpen?: boolean
  children: React.ReactNode
}

export const CollapsibleSection = ({
  title,
  count,
  defaultOpen = true,
  children,
}: Props) => {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className="mt-6">
      
      {/* HEADER */}
      <button
        onClick={() => setOpen(!open)}
        className="
          w-full flex justify-between items-center
          text-left
        "
      >
        <h2 className="text-2xl font-semibold flex items-center gap-2">
          {title}
          {count !== undefined && (
            <span className="text-m opacity-70">
              {count}
            </span>
          )}
        </h2>

        {open ? (
          <ChevronDown size={18} />
        ) : (
          <ChevronRight size={18} />
        )}
      </button>

      {/* CONTENT */}
      {open && (
        <div className="mt-2">
          {children}
        </div>
      )}
    </div>
  )
}