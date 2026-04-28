import { Flag, Sailboat, Boxes, University, Calendar } from "lucide-react"

export const nav_links = [
  {
    to: "/regattas",
    label: "Regattas",
    icon: Flag,
  },
  {
    to: "/boats",
    label: "Boats",
    icon: Sailboat,
  },
  {
    to: "/classes",
    label: "Classes",
    icon: Boxes,
  },
  {
    to: "/clubs",
    label: "Clubs",
    icon: University,
  },
  {
    to: "/calendar",
    label: "Calendar",
    icon: Calendar,
  }
]