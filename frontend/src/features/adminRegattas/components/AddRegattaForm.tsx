import { useState } from "react"
import type { AdminRegattaOptions, CreateAdminRegattaQueueItem } from "../types"

type Props = {
    options: AdminRegattaOptions
    adding: boolean
    onAdd: (data: CreateAdminRegattaQueueItem) => Promise<void>
}

const currentYear = new Date().getFullYear()

export const AddRegattaForm = ({ options, adding, onAdd }: Props) => {
    const [open, setOpen] = useState(false)
    const [form, setForm] = useState<CreateAdminRegattaQueueItem>({
        regatta_name: "",
        year: currentYear,
        type: "",
        status: "past",
        scraper_name: "",
        scrape_active: 0,
        source_type: "",
        scrape_status: "",
        specified_class: "",
        start_date: "",
        end_date: "",
        notes: "",
        city: "",
        region: "",
        country: "",
        link: ""
    })
    const [success, setSuccess] = useState(false)

    const updateField = (
        key: keyof CreateAdminRegattaQueueItem,
        value: string | number
    ) => {
        setForm((current) => ({
            ...current,
            [key]: value
        }))
        setSuccess(false)
    }

    const handleSubmit = async () => {
        if (!form.regatta_name || !form.year) return

        await onAdd(form)
        setSuccess(true)
        setForm({
            regatta_name: "",
            year: currentYear,
            type: "",
            status: "past",
            scraper_name: "",
            scrape_active: 0,
            source_type: "",
            scrape_status: "",
            specified_class: "",
            start_date: "",
            end_date: "",
            notes: "",
            city: "",
            region: "",
            country: "",
            link: ""
        })
    }

    return (
        <div
            className="
                p-4 rounded-xl
                border border-border dark:border-borderDark
                bg-background dark:bg-backgroundDark
                space-y-4
            "
        >
            <div className="flex justify-between items-center gap-3">
                <div>
                    <h2 className="font-semibold">Add regatta to scrape queue</h2>
                    <p className="text-sm opacity-70">
                        This writes a new row to scrape_queue.csv
                    </p>
                </div>

                <button
                    onClick={() => setOpen(!open)}
                    className="
                        text-sm px-3 py-1 rounded-xl
                        border border-border dark:border-borderDark
                        hover:bg-primary hover:text-white
                        transition-colors
                    "
                >
                    {open ? "Close" : "Add"}
                </button>
            </div>

            {open && (
                <div className="space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Regatta name</span>
                            <input
                                value={form.regatta_name}
                                onChange={(e) => updateField("regatta_name", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Year</span>
                            <input
                                type="number"
                                value={form.year}
                                onChange={(e) => updateField("year", Number(e.target.value))}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Type</span>
                            <input
                                value={form.type || ""}
                                onChange={(e) => updateField("type", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Status</span>
                            <input
                                value={form.status || ""}
                                onChange={(e) => updateField("status", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Start date</span>
                            <input
                                type="date"
                                value={form.start_date || ""}
                                onChange={(e) => updateField("start_date", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">End date</span>
                            <input
                                type="date"
                                value={form.end_date || ""}
                                onChange={(e) => updateField("end_date", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Scraper</span>
                            <select
                                value={form.scraper_name || ""}
                                onChange={(e) => updateField("scraper_name", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            >
                                <option value="">Select scraper</option>
                                {options.scrapers.map((scraper) => (
                                    <option key={scraper} value={scraper}>
                                        {scraper}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Source type</span>
                            <select
                                value={form.source_type || ""}
                                onChange={(e) => updateField("source_type", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            >
                                <option value="">Select source type</option>
                                {options.source_types.map((sourceType) => (
                                    <option key={sourceType} value={sourceType}>
                                        {sourceType}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Specified class</span>
                            <input
                                value={form.specified_class || ""}
                                onChange={(e) => updateField("specified_class", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">City</span>
                            <input
                                value={form.city || ""}
                                onChange={(e) => updateField("city", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Region</span>
                            <input
                                value={form.region || ""}
                                onChange={(e) => updateField("region", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Country</span>
                            <input
                                value={form.country || ""}
                                onChange={(e) => updateField("country", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>
                    </div>

                    <label className="space-y-1 text-sm block">
                        <span className="font-medium">Link</span>
                        <input
                            value={form.link || ""}
                            onChange={(e) => updateField("link", e.target.value)}
                            className="
                                w-full p-2 rounded-lg
                                border border-border dark:border-borderDark
                                bg-background dark:bg-backgroundDark
                            "
                        />
                    </label>

                    <label className="space-y-1 text-sm block">
                        <span className="font-medium">Notes</span>
                        <textarea
                            value={form.notes || ""}
                            onChange={(e) => updateField("notes", e.target.value)}
                            className="
                                w-full p-2 rounded-lg
                                border border-border dark:border-borderDark
                                bg-background dark:bg-backgroundDark
                                min-h-20
                            "
                        />
                    </label>

                    <div className="flex justify-between items-center gap-3">
                        <label className="flex items-center gap-2 text-sm">
                            <input
                                type="checkbox"
                                checked={form.scrape_active === 1}
                                onChange={(e) => updateField("scrape_active", e.target.checked ? 1 : 0)}
                            />
                            <span>Active for scraping</span>
                        </label>

                        <div className="flex items-center gap-3">
                            {success && (
                                <span className="text-sm text-green-600">
                                    Added to queue
                                </span>
                            )}

                            <button
                                disabled={adding || !form.regatta_name || !form.year}
                                onClick={handleSubmit}
                                className="
                                    px-4 py-2 rounded-lg
                                    bg-primary dark:bg-primaryDark
                                    text-white
                                    disabled:opacity-50
                                "
                            >
                                {adding ? "Adding..." : "Add to queue"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
