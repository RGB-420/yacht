import { Link } from "react-router-dom"
import { House, Menu, X } from "lucide-react"
import { NavLinks } from "./NavLinks"
import { ThemeToggle } from "./ThemeToggle"
import { useState } from "react"

export const Navbar = () => {
  const [open, setOpen] = useState(false)

  return (
    <div className="
      relative px-4 py-3 flex items-center
      bg-surface dark:bg-surfaceDark
      border-b border-border dark:border-borderDark
    ">

      {/* LEFT */}
      <div className="flex items-center gap-4">

        {/* MÓVIL → HAMBURGER */}
        <button
          className="sm:hidden"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>

        {/* DESKTOP → NAV LINKS */}
        <div className="hidden sm:flex gap-6">
          <NavLinks />
        </div>

      </div>

      {/* LOGO CENTRO */}
      <Link
        to="/"
        className="
          absolute left-1/2 -translate-x-1/2
          flex items-center gap-2
          text-text dark:text-textDark
        "
      >
        <House size={20} />
        <span className="font-semibold">
          Regatta Explorer
        </span>
      </Link>

      {/* RIGHT → SOLO THEME */}
      <div className="ml-auto">
        <ThemeToggle />
      </div>

      {/* MOBILE MENU */}
      {open && (
        <div className="
          absolute top-full left-0 w-full
          bg-surface/90 dark:bg-surfaceDark/90
          backdrop-blur-md
          border-t border-border dark:border-borderDark
          shadow-xl
          flex flex-col items-center gap-4 py-4
          sm:hidden
          z-50
        ">
          <NavLinks onClick={() => setOpen(false)} />
        </div>
      )}
    </div>
  )
}