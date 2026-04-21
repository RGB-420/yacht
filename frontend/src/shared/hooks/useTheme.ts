import { useEffect, useState } from "react"

export const useTheme = () => {
    const [theme, setTheme] = useState<"light" | "dark">(() => {
        const saved = localStorage.getItem("theme") as "light" | "dark" | null
        return saved || "light"
    })

    useEffect(() => {
        if (theme === "dark") {
            document.documentElement.classList.add("dark") 
        } else {
            document.documentElement.classList.remove("dark")
        }

        localStorage.setItem("theme", theme)
    }, [theme])

    const toggleTheme = () => {
        setTheme(prev => (prev === "light" ? "dark" : "light"))
    }

    return { theme, toggleTheme}
}