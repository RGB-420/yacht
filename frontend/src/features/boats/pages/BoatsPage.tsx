import { useBoats } from "../hooks/useBoats"
import { BoatItem } from "../components/BoatItem"
import { useState } from "react"
import { PaginationControls } from "../../../shared/components/PaginationControls"

export const BoatsPage = () => {
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(50)

  const { boats, total, loading, error } = useBoats(page, limit)

  if (loading) return <p className="p-4">Loading...</p>
  if (error) return <p className="p-4">{error}</p>

  return (
    <div className="p-4 space-y-4">
      
      <h1 className="text-2xl font-bold">Boats</h1>

      <ul className="space-y-2">
        {boats.map((boat) => (
          <BoatItem key={boat.id_boat} boat={boat} />
        ))}
      </ul>

      <PaginationControls
        page={page}
        total={total}
        limit={limit}
        onPageChange={setPage}
        onLimitChange={setLimit}
        pageSizeOptions={[25, 50, 100, 200]}
      />

    </div>
  )
}