import { Link } from "react-router-dom"
import { nav_links } from "../config/navigation"

export const NavLinks = ({ onClick }: { onClick?: () => void }) => {
  return (
    <>
      {nav_links.map((item) => {
        const Icon = item.icon

        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={onClick}
            className="
              flex flex-col items-center text-sm
              text-text dark:text-textDark
              hover:opacity-70
              transition
            "
          >
            <Icon size={20} />

            <span className="py-1 text-xs font-medium">
              {item.label}
            </span>
          </Link>
        )
      })}
    </>
  )
}