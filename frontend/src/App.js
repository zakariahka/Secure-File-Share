import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Root from "./pages/Root";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import FilesPage from "./pages/FilesPage";
import { UserProvider } from "./context/UserContext";
import PublicRoute from "./components/PublicRoute";
import ProtectedRoute from "./components/ProtectedRoute";
import CatchAllRoutes from "./components/CatchAllRoutes";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "/",
        element: <PublicRoute />,
        children: [
          { path: "/login", element: <LoginPage />},
          { path: "/signup", element: <SignUpPage />},
          { path: "/forgot-password", element: <ForgotPasswordPage />},
        ]
      },
      {
        path: "/",
        element: <ProtectedRoute />,
        children: [
          { path: "/files", element: <FilesPage />}
        ]
      },
      {
        path: "*",
        element: <CatchAllRoutes />
      }
    ]
  },
]);

function App() {
  return (
    <UserProvider>
        <RouterProvider router={router} />
    </UserProvider>
  );
}

export default App;