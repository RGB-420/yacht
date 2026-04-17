interface Props {
    page: number
    total: number
    limit: number
    onPageChange: (page: number) => void
}

import {
    ChevronLeft,
    ChevronRight,
    ChevronsLeft,
    ChevronsRight
} from "lucide-react"

export const Pagination = ({ page, total, limit, onPageChange }: Props) => {
    const totalPages = Math.ceil(total / limit)

    const getPageNumbers = () => {
        const totalPages = Math.ceil(total / limit)
        const pages = []
        
        const windowSize = 4

        const start = Math.max(1, page - windowSize)
        const end = Math.min(totalPages, page + windowSize)

        for (let i = start; i <= end; i++) {
            pages.push(i)
        }

        return pages
    }

    return (
        <div className="flex justify-center mt-4">
            <div className="flex border rounded-lg overflow-hidden">

            {/* Primera página */}
            <button
                onClick={() => onPageChange(1)}
                disabled={page === 1}
                className="p-2 disabled:opacity-50"
            >
                <ChevronsLeft size={20} />
            </button>

            {/* Prev */}
            <button
                onClick={() => onPageChange(page - 1)}
                disabled={page === 1}
                className="p-2 disabled:opacity-50"
            >
                <ChevronLeft size={18} />
            </button>

            {/* Info */}
            {getPageNumbers().map((p) => (
            <button
                key={p}
                onClick={() => onPageChange(p)}
                className={`px-3 py-2 border-r ${
                p === page
                    ? "bg-blue-600 text-white"
                    : "hover:bg-gray-100"
                }`}
            >
                {p}
            </button>
            ))}

            {/* Siguiente */}
            <button
                onClick={() => onPageChange(page + 1)}
                disabled={page === totalPages}
                className="p-2 disabled:opacity-50"
            >
                <ChevronRight size={18} />
            </button>

            {/* Última página */}
            <button
                onClick={() => onPageChange(totalPages)}
                disabled={page === totalPages}
                className="p-2 disabled:opacity-50"
            >
                <ChevronsRight size={20} />
            </button>
            </div>
        </div>
    )
}