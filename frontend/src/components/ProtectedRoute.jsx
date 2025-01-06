import { useContext } from "react";
import { UserContext } from "../context/UserContext";
import { Navigate, Outlet } from "react-router-dom";
 
const ProtectedRoute = () => {
    const { userData, isLoading } = useContext(UserContext);

    if(isLoading){
        return <div>Loading.....</div>
    }

    return userData ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute