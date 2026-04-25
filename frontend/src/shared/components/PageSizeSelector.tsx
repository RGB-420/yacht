interface Props {
  value: number
  options: number[]
  onChange: (value: number) => void
}

export const PageSizeSelector = ({ value, options, onChange }: Props) => {
  return (
    <div className="flex items-center justify-center gap-3 mt-1">

        <p className="text-s text-gray-400">
            Page size
        </p>

      <div className="inline-flex border border-border dark:border-borderDark rounded-lg overflow-hidden">
        {options.map((opt) => (
          <button
            key={opt}
            onClick={() => onChange(opt)}
            className={`px-2 py-1 text-sm ${
              value === opt
                ? "bg-primary text-textDark"
                : "bg-background dark:bg-backgroundDark hover:bg-border dark:hover:bg-borderDark"
            }`}
          >
            {opt}
          </button>
        ))}
      </div>

    </div>
  )
}