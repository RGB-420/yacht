import { useParams, Link } from "react-router-dom"
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
                    entityType="boat"
                    entityId={Number(id)}
                />
            </div>
        </div>


      <div className="space-y-4">
        {boat.boat_identifier && (
          <p><strong>Identifier:</strong> {boat.boat_identifier}</p>
        )}

        {boat.classes.length > 0 && (
          <div>
            <h2 className="font-semibold">Classes</h2>

            <div className="flex flex-wrap gap-2 mt-2">
              {boat.classes.map((className, i) => (
                <Link
                  key={i}
                  to={`/classes/${boat.class_ids[i]}`}
                  className="px-2 py-1 text-sm border rounded-lg hover:bg-primary hover:text-white transition"
                >
                  {className}
                </Link>
              ))}
            </div>
          </div>
        )}

        {boat.types.length > 0 && (
          <div>
            <h2 className="font-semibold">Types</h2>

            <div className="flex flex-wrap gap-2 mt-2">
              {boat.types.map((type, i) => (
                <span
                  key={i}
                  className="px-2 py-1 text-sm border rounded-lg"
                >
                  {type}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {boat.owners.length > 0 && (
        <div>
          <h2 className="font-semibold">Owners</h2>

          <div className="flex flex-wrap gap-2 mt-2">
            {boat.owners.map((owner, i) => (
              <span
                key={i}
                className="px-2 py-1 text-sm border rounded-lg"
              >
                {owner}
              </span>
            ))}
          </div>
        </div>
      )}

      {boat.clubs.length > 0 && (
        <div>
          <h2 className="font-semibold">Clubs</h2>
          
          <div className="flex flex-wrap gap-2 mt-2">
            {boat.clubs.map((club, i) => (
              <Link
                key={i}
                to={`/clubs/${boat.club_ids[i]}`}
                className="px-2 py-1 text-sm border rounded-lg hover:bg-primary"
              >
                {club}
              </Link>
            ))}
          </div>
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
