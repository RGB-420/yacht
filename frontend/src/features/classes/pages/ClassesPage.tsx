import { useClasses } from "../hooks/useClasses"
import { ClassItem } from "../components/ClassItem" 
import { ClipLoader } from "react-spinners"

export const ClassesPage = () => {

  const { classes, loading, error } = useClasses()

  if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
  if (error) return <p className="p-4">{error}</p>

  return (
    <div className="p-4 space-y-4">
      
      <h1 className="text-2xl font-bold">Classes</h1>

      <ul className="space-y-2">
        {classes.map((cls) => (
          <ClassItem key={cls.id_class} cls={cls} />
        ))}
      </ul>
    </div>
  )
}