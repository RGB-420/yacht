interface Props {
  value: number
  options: number[]
  onChange: (value: number) => void
}

export const PageSizeSelector = ({ value, options, onChange }: Props) => {
  return (
    <div className="flex items-center justify-center gap-3 mt-1">

        <p className="text-xs text-gray-400">
            Page size
        </p>

      <div className="inline-flex border rounded-lg overflow-hidden">
        {options.map((opt) => (
          <button
            key={opt}
            onClick={() => onChange(opt)}
            className={`px-2 py-1 text-sm ${
              value === opt
                ? "bg-blue-600 text-white"
                : "bg-white text-blue-600 hover:bg-gray-100"
            }`}
          >
            {opt}
          </button>
        ))}
      </div>

    </div>
  )
}