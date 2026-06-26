import { Routes, Route } from "react-router-dom"
import { HomePage } from "../features/home/pages/HomePage"
import { RegattasPage } from "../features/regattas/pages/RegattasPage"
import { RegattaDetailPage } from "../features/regattas/pages/RegattaDetailPage"
import { EditionDetailPage } from "../features/editions/pages/EditionDetailPage"
import { BoatDetailPage } from "../features/boats/pages/BoatDetailPage"
import { BoatsPage } from "../features/boats/pages/BoatsPage"
import { ClassesPage } from "../features/classes/pages/ClassesPage"
import { ClassDetailPage } from "../features/classes/pages/ClassDetailPage"
import { ClubsPage } from "../features/clubs/pages/ClubsPage"
import { ClubDetailPage } from "../features/clubs/pages/ClubDetailPage"
import { CalendarPage } from "../features/schedules/pages/CalendarPage"
import { FeedbackPage } from "../features/feedback/pages/FeedbackPage"
import { AdminPage } from "../features/admin/pages/AdminPage"
import { AdminCorrectionsPage } from "../features/admin/pages/AdminCorrectionsPage"
import { QualityDashboardPage } from "../features/quality/pages/QualityDashboardPage"
import { QualityIssuePage } from "../features/quality/pages/QualityIssuePage"
import { AdminRegattasPage } from "../features/adminRegattas/pages/AdminRegattasPage"
import { AdminClubCorrectionsPage } from "../features/adminClubCorrections/pages/AdminClubCorrectionsPage"
import { AdminClassTypeCorrectionsPage } from "../features/adminClassTypeCorrections/pages/AdminClassTypeCorrectionsPage"
import { AdminOwnerCorrectionsPage } from "../features/adminOwnerCorrections/pages/AdminOwnerCorrectionsPage"

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

            <Route path="/classes/:id" element={<ClassDetailPage />} />

            <Route path="/clubs" element={<ClubsPage />} />

            <Route path="/clubs/:id" element={<ClubDetailPage />} />

            <Route path="/calendar" element={<CalendarPage />} />

            <Route path="/admin" element={<AdminPage />} />

            <Route path="/admin/feedback" element={<FeedbackPage />} />

            <Route path="/admin/quality" element={<QualityDashboardPage />} />

            <Route path="/admin/quality/boats/issues/:issueKey" element={<QualityIssuePage />} />

            <Route path="/admin/regattas" element={<AdminRegattasPage />} />

            <Route path="/admin/corrections" element={<AdminCorrectionsPage />} />

            <Route path="/admin/corrections/clubs" element={<AdminClubCorrectionsPage />} />

            <Route path="/admin/corrections/class-types" element={<AdminClassTypeCorrectionsPage />} />

            <Route path="/admin/corrections/owners" element={<AdminOwnerCorrectionsPage />} />
        </Routes>
    )
}
