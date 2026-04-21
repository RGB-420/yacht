import { useTheme } from "../hooks/useTheme"
import { Moon, Sun } from "lucide-react"

export const ThemeToggle = () => {
    const { theme, toggleTheme } = useTheme()

    return (
        <button
            onClick={toggleTheme}
            className="px-2 py-1 text-sm hover:opacity-70"
        >
            {theme === "dark" ? <Moon size={30}/> : <Sun size={30}/>}
        </button>
    )
}