import { Pagination } from "./Pagination"
import { PageSizeSelector } from "./PageSizeSelector"

interface Props {
    page: number
    total: number
    limit: number
    onPageChange: (page: number) => void
    onLimitChange: (limit: number) => void,
    pageSizeOptions?: number[]
}

export const PaginationControls = ({
    page, total, limit,
    onPageChange, onLimitChange, pageSizeOptions
}: Props) => {
    const options = pageSizeOptions ?? [25, 50, 100, 200]

    return (
        <div className="space-y-3">
            <Pagination
                page={page}
                total={total}
                limit={limit}
                onPageChange={onPageChange}
            />

            <PageSizeSelector
                value={limit}
                options={options}
                onChange={(newLimit) => {
                onLimitChange(newLimit)
                onPageChange(1) 
                }}
            />
        </div>
    )
}