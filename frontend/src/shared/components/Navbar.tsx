import { Link } from "react-router-dom"
import { House, Sailboat, Flag } from "lucide-react"

import { ThemeToggle } from "./ThemeToggle"

export const Navbar = () => {
  return (
    <div className="relative px-6 py-4 flex items-center 
      bg-surface dark:bg-surfaceDark 
      border-b border-border dark:border-borderDark 
      transition-colors"
    >
      <ThemeToggle />

      <Link
        to="/"
        className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2 
        text-text dark:text-textDark 
        hover:opacity-70 transition"
      >
        <House size={20} className="text-text dark:text-textDark" />

        <span className="font-semibold">
          Regatta Explorer
        </span>
      </Link>
    
      <div className="ml-auto flex items-center gap-6">

        <Link
          to="/regattas"
          className="flex flex-col items-center text-sm 
          text-text dark:text-textDark
          hover:opacity-70
          transition"
        >
          <Flag size={20} />

          <span className="py-1 text-xs font-medium">
            Regattas
          </span>
        </Link>

        <Link
          to="/boats"
          className="flex flex-col items-center text-sm 
          text-text dark:text-textDark
          hover:opacity-70
          transition"
        >
          <Sailboat size={20} />

          <span className="py-1 text-xs font-medium">
            Boats
          </span>
        </Link>

      </div>
    </div>
  )
}