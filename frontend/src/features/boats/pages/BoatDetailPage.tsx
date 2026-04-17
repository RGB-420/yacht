import { useParams } from "react-router-dom"
import { useBoat } from "../hooks/useBoat"
import { useBoatEditions } from "../hooks/useBoatsEditions"
import { EditionBoatItem } from "../../editions/components/EditionBoatItem"

export const BoatDetailPage = () => {
    const { id } = useParams()

    const { boat, loading, error } = useBoat(id)
    const { editions, loading: loadingEditions } = useBoatEditions(id)

    if (loading) return <p className="p-4">Loading...</p>
    if (error) return <p className="p-4">{error}</p>
    if (!boat) return <p className="p-4">No data</p>

    return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">{boat.name}</h1>

      <div className="space-y-1">
        {boat.boat_identifier && (
          <p><strong>Identifier:</strong> {boat.boat_identifier}</p>
        )}

        {boat.class_name && (
          <p><strong>Class:</strong> {boat.class_name}</p>
        )}

        {boat.type_name && (
          <p><strong>Type:</strong> {boat.type_name}</p>
        )}
      </div>

      {boat.owners.length > 0 && (
        <div>
          <h2 className="font-semibold">Owners</h2>
          <ul className="list-disc ml-5">
            {boat.owners.map((owner, i) => (
              <li key={i}>{owner}</li>
            ))}
          </ul>
        </div>
      )}

      {boat.clubs.length > 0 && (
        <div>
          <h2 className="font-semibold">Clubs</h2>
          <ul className="list-disc ml-5">
            {boat.clubs.map((club, i) => (
              <li key={i}>{club}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Participations</h2>

        {loadingEditions && <p>Loading...</p>}

        {!loadingEditions && editions.length === 0 && (
          <p>No participations found</p>
        )}

        <ul className="mt-2 space-y-2">
          {editions.map((ed) => (
            <EditionBoatItem key={ed.id_edition} edition={ed} />
          ))}
        </ul>
      </div>
    </div>
  )
}