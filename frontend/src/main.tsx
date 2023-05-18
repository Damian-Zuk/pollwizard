import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { AuthProvider } from 'react-auth-kit';
import Home from './pages/Home'
import Login from './pages/Login'
import logout from './pages/Logout'
import Profile from './pages/Profile'
import Navbar from './components/Navbar'
import 'bootstrap/dist/css/bootstrap.css'
import "./styles/main.css"
import Logout from './pages/Logout';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/home",
    element: <Home />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/logout",
    element: <Logout />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <AuthProvider authType = {'cookie'}
                  authName={'_auth'}
                  cookieDomain={window.location.hostname}
                  cookieSecure={window.location.protocol === "https:"}>
      <Navbar />
      <RouterProvider router={router} />
    </AuthProvider>
  </React.StrictMode>,
)
