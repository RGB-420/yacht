import { useParams } from "react-router-dom"
import { useClub } from "../hooks/useClub"
import { ClipLoader } from "react-spinners"
import { useClubBoats } from "../hooks/useClubBoats"
import { BoatItem } from "../../boats/components/BoatItem"
import { useClubRegattas } from "../hooks/useClubRegattas"
import { RegattaItem } from "../../regattas/components/RegattaItem"

import { CollapsibleSection } from "../../../shared/components/CollapsibleSection"

export const ClubDetailPage = () => {
    const { id } = useParams()

    const { club, loading, error } = useClub(id)
    const { boats, loading: loadingBoats } = useClubBoats(id)
    const { regattas, loading: loadingRegattas } = useClubRegattas(id)

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>

    if (!club) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-4">
            <h1 className="text-2xl font-bold">{club.name}</h1>

            <div className="space-y-1">
                {club.short_name && <p><strong>Short name:</strong> {club.short_name}</p>}
                {club.estimated_numbers && <p><strong>Estimated members:</strong> {club.estimated_numbers}</p>}
                {club.city && <p><strong>City:</strong> {club.city}</p>}
                {club.region && <p><strong>Region:</strong> {club.region}</p>}
                {club.country && <p><strong>Country:</strong> {club.country}</p>}

                <CollapsibleSection title="Boats" count={club.number_of_boats}>

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

                <CollapsibleSection title="Organized Regattas" count={club.number_of_regattas}>

                    {loadingRegattas && <p>Loading regattas...</p>}

                    {!loadingRegattas && regattas.length === 0 && (
                        <p>No regattas found</p>
                    )}

                    <ul className="mt-2 space-y-2">
                        {regattas.map((regatta) => (
                            <RegattaItem key={regatta.id_regatta} regatta={regatta}/>
                        ))}
                    </ul>
                </CollapsibleSection>
            </div>


        </div>
    )
}