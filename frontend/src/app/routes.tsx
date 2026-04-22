import { Routes, Route } from "react-router-dom"
import { HomePage } from "../features/home/pages/HomePage"
import { RegattasPage } from "../features/regattas/pages/RegattasPage"
import { RegattaDetailPage } from "../features/regattas/pages/RegattaDetailPage"
import { EditionDetailPage } from "../features/editions/pages/EditionDetailPage"
import { BoatDetailPage } from "../features/boats/pages/BoatDetailPage"
import { BoatsPage } from "../features/boats/pages/BoatsPage"
import { ClassesPage } from "../features/classes/pages/ClassesPage"
import { ClubsPage } from "../features/clubs/pages/ClubsPage"

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<HomePage />} />
            
            <Route path="/regattas" element={<RegattasPage />} />

            <Route path="/regattas/:id" element={<RegattaDetailPage />} />

            <Route path="/editions/:id" element={<EditionDetailPage />} />

            <Route path="/boats" element={<BoatsPage />} />

            <Route path="/boats/:id" element={<BoatDetailPage />} />

            <Route path="/classes" element={<ClassesPage />} />

            <Route path="/clubs" element={<ClubsPage />} />
        </Routes>
    )
}