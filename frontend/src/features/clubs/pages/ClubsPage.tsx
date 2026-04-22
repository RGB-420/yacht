import { useClubs } from "../hooks/useClubs"
import { ClubItem } from "../components/ClubItem"
import { ClipLoader } from "react-spinners"

export const ClubsPage = () => {

    const { clubs, loading, error } = useClubs()

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>

    return (
    <div className="p-4 space-y-4">
        
        <h1 className="text-2xl font-bold">Clubs</h1>

        <ul className="space-y-2">
        {clubs.map((club) => (
            <ClubItem key={club.id_club} club={club} />
        ))}
        </ul>
    </div>
    )
}