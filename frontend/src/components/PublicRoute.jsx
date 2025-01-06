import { useContext } from "react";
import { UserContext } from "../context/UserContext";
import { Navigate, Outlet } from "react-router-dom";

const PublicRoute = () => {
  const { userData, isLoading } = useContext(UserContext);

  if (isLoading) {
    return <div>Loading.....</div>;
  }

  return userData ? <Navigate to="/files" replace /> : <Outlet />;
};

export default PublicRoute;
