import { UserContext } from "../context/UserContext"
import { useContext } from "react"
import { Navigate } from "react-router-dom"

const CatchAllRoutes = () => {
    const { isLoading, userData } = useContext(UserContext)

    if (isLoading){
        return <div>Loading....</div>
    }
    if(userData){
        return <Navigate to='/files' replace />
    }else{
        return <Navigate to='login' replace />
    }
}

export default CatchAllRoutes;