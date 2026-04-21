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
            <div className="flex border border-border dark:border-borderDark rounded-lg overflow-hidden">

            {/* Primera página */}
            <button
                onClick={() => onPageChange(1)}
                disabled={page === 1}
                className="p-2 border border-border dark:border-borderDark disabled:opacity-50 hover:bg-border dark:hover:bg-borderDark"
            >
                <ChevronsLeft size={20} />
            </button>

            {/* Prev */}
            <button
                onClick={() => onPageChange(page - 1)}
                disabled={page === 1}
                className="p-2 border border-border dark:border-borderDark disabled:opacity-50 hover:bg-border dark:hover:bg-borderDark"
            >
                <ChevronLeft size={18} />
            </button>

            {/* Info */}
            {getPageNumbers().map((p) => (
            <button
                key={p}
                onClick={() => onPageChange(p)}
                className={`px-3 py-2 border border-border dark:border-borderDark ${
                p === page
                    ? "bg-primary text-white"
                    : "hover:bg-border dark:hover:bg-borderDark"
                }`}
            >
                {p}
            </button>
            ))}

            {/* Siguiente */}
            <button
                onClick={() => onPageChange(page + 1)}
                disabled={page === totalPages}
                className="p-2 border border-border dark:border-borderDark disabled:opacity-50 hover:bg-border dark:hover:bg-borderDark"
            >
                <ChevronRight size={18} />
            </button>

            {/* Última página */}
            <button
                onClick={() => onPageChange(totalPages)}
                disabled={page === totalPages}
                className="p-2 border border-border dark:border-borderDark disabled:opacity-50 hover:bg-border dark:hover:bg-borderDark"
            >
                <ChevronsRight size={20} />
            </button>
            </div>
        </div>
    )
}