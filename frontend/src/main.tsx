import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { AuthProvider } from 'react-auth-kit';

import Home from './pages/Home'
import Login from './pages/Login'
import Profile from './pages/Profile'
import Logout from './pages/Logout';
import SignUp from './pages/Singup';

import Navbar from './components/Navbar'
import 'bootstrap/dist/css/bootstrap.css'
import "./styles/main.css"

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
  {
    path: "/signup",
    element: <SignUp />,
  },
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <AuthProvider authType = {'cookie'}
                authName={'_auth'}
                cookieDomain={window.location.hostname}
                cookieSecure={window.location.protocol === "https:"}>
    <Navbar />
    <RouterProvider router={router} />
  </AuthProvider>,
)
