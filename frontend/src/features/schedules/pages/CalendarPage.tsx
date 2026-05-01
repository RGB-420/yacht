import { useSchedule } from "../hooks/useSchedule"
import { ClipLoader } from "react-spinners"
import { ScheduleCalendar } from "../components/ScheduleCalendar"
import { SuggestRegattaButton } from "../../feedback/components/SuggestRegattaButton"
export const CalendarPage = () => {
    const { events, loading, error } = useSchedule()

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>

    return (
        <div className="
            mt-4 sm:mt-6
            w-full
            max-w-full
            bg-background dark:bg-backgroundDark
            p-2 sm:p-4
            rounded-xl sm:rounded-2xl
            shadow-lg
            border border-border dark:border-borderDark
        ">
            <div className="flex items-center">
                <h1 className="text-2xl font-bold">
                    Calendar
                </h1>
                <div className="ml-auto">
                    < SuggestRegattaButton />
                </div>
            </div>

            <ScheduleCalendar events={events} />
        </div>
    )
}