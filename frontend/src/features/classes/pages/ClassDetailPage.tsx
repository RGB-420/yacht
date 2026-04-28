import { useParams } from "react-router-dom"
import { useClass } from "../hooks/useClass"
import { ClipLoader } from "react-spinners"
import { useClassBoat } from "../hooks/useClassBoats"
import { BoatItem } from "../../boats/components/BoatItem"
import { CollapsibleSection } from "../../../shared/components/CollapsibleSection"
import { FeedbackButton } from "../../feedback/components/FeedbackButton"

export const ClassDetailPage = () => {
    const { id } = useParams()

    const { class_, loading, error } = useClass(id)
    const { boats, loading: loadingBoats } = useClassBoat(id)

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>

    if (!class_) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-4">
            <div className="flex items-center">
                <h1 className="text-2xl font-bold">
                    {class_.name}
                </h1>
                <div className="ml-auto">
                    <FeedbackButton
                        entityType="class"
                        entityId={Number(id)}
                    />
                </div>
            </div>
            

            <div className="space-y-1">
                {class_.category && <p><strong>Category:</strong> {class_.category}</p>}
                {class_.manufacturer && <p><strong>Manufacturer:</strong> {class_.manufacturer}</p>}
                {class_.rating_rule && <p><strong>Rating rule:</strong> {class_.rating_rule}</p>}
                {class_.start_year && <p><strong>Start year:</strong> {class_.start_year}</p>}
                {class_.crew_min && (
                    <p>
                        <strong>Crew:</strong>{" "}
                        {class_.crew_min === class_.crew_max
                            ? class_.crew_min
                            : `${class_.crew_min}-${class_.crew_max}`}
                    </p>
                )}
                {class_.length_m && <p><strong>Length:</strong> {class_.length_m} m</p>}

                <CollapsibleSection title="Boats" count={class_.number_of_boats}>

                    {loadingBoats && <p>Loading boats...</p>}

                    {!loadingBoats && boats.length === 0 && (
                        <p>No boats found</p>
                    )}

                    <ul className="mt-2 space-y-2">
                        {boats.map((boat) => (
                            <BoatItem key={boat.id_boat} boat={boat}/>
                        ))}
                    </ul>
                </CollapsibleSection>
            </div>
        </div>
    )
}