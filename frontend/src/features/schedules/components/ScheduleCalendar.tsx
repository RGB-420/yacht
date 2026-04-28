import FullCalendar from "@fullcalendar/react"
import dayGridPlugin from "@fullcalendar/daygrid"
import { useNavigate } from "react-router-dom"
import type { ScheduleEvent } from "../types"

type Props = {
    events: ScheduleEvent[]
}

export const ScheduleCalendar = ({ events }: Props) => {
    const navigate = useNavigate()

    const calendarEvents = events.map((event) => ({
        id: String(event.id_edition),
        title: `${event.regatta_name} (${event.year})`,
        start:event.start_date,
        end: event.end_date,
    }))

    return (
        <FullCalendar
            plugins={[dayGridPlugin]}
            initialView="dayGridMonth"
            events={calendarEvents}
            eventClick={(info) => {
                navigate(`/editions/${info.event.id}`)
            }}
            dayMaxEventRows={2}
            eventClassNames={() => [
                "rounded-md",
                "px-2",
                "py-1",
                "text-xs",
                "font-medium",
                "bg-primary",
                "text-white",
                "hover:bg-primary/80",
                "border-none"
            ]}
            height="auto"
            contentHeight="auto"
            expandRows={true}
        />
    )
}