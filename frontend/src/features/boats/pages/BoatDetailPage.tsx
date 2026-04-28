import { useParams } from "react-router-dom"
import { useBoat } from "../hooks/useBoat"
import { useBoatEditions } from "../hooks/useBoatsEditions"
import { EditionBoatItem } from "../../editions/components/EditionBoatItem"
import { ClipLoader } from "react-spinners"
import { CollapsibleSection } from "../../../shared/components/CollapsibleSection"
import { FeedbackButton } from "../../feedback/components/FeedbackButton"

export const BoatDetailPage = () => {
    const { id } = useParams()

    const { boat, loading, error } = useBoat(id)
    const { editions, loading: loadingEditions } = useBoatEditions(id)

    if (loading) 
      return (
          <div className="flex justify-center items-center p-10">
              <ClipLoader size={30} color={"#3b82f6"} />
          </div>
      )
    if (error) return <p className="p-4">{error}</p>
    if (!boat) return <p className="p-4">No data</p>

    return (
    <div className="p-4 space-y-4">
        <div className="flex items-center">
            <h1 className="text-2xl font-bold">
                {boat.name}
            </h1>
            <div className="ml-auto">
                <FeedbackButton
                    entityType="edition"
                    entityId={Number(id)}
                />
            </div>
        </div>


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

      <CollapsibleSection title="Participations" >

        {loadingEditions && <p>Loading...</p>}

        {!loadingEditions && editions.length === 0 && (
          <p>No participations found</p>
        )}

        <ul className="mt-2 space-y-2">
          {editions.map((ed) => (
            <EditionBoatItem key={ed.id_edition} edition={ed} />
          ))}
        </ul>
      </CollapsibleSection>
    </div>
  )
}