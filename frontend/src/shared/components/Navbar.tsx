import { Link } from "react-router-dom"
import { House, Sailboat, Flag } from "lucide-react"

export const Navbar = () => {
  return (
    <div className="relative border-b px-6 py-4 flex items-center">

      <Link
        to="/"
        className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2 hover:opacity-70 transition"
      >
        <House size={20} />
        <span className="font-semibold">
            Regatta Explorer
        </span>
        </Link>
    
        <div className="ml-auto flex items-center gap-6">

        <Link
        to="/regattas"
        className="flex flex-col items-center text-sm text-gray-600 hover:text-black transition"
        >
        <Flag size={18} />
        <span className="text-xs font-medium">
            Regattas
        </span>
        </Link>

        <Link
            to="/boats"
            className="flex flex-col items-center text-sm text-gray-600 hover:text-black transition"
        >
            <Sailboat size={20} />

            <span className="text-xs font-medium">
                Boats
            </span>
        </Link>



        </div>
    </div>
  )
}