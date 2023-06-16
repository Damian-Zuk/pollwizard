import 'bootstrap/dist/css/bootstrap.css'
import "react-toastify/dist/ReactToastify.css"
import 'react-confirm-alert/src/react-confirm-alert.css';
import "./styles/main.css"

import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { AuthProvider } from 'react-auth-kit';
import { ToastContainer } from 'react-toastify';
import axios from 'axios';
import { lazy, Suspense } from "react";

import refreshApi from './auth/RefreshApi';
import Navbar from './components/Navbar'

axios.defaults.baseURL = "http://localhost:8000/"

const Home = lazy(() => import("./pages/Home"))
const Login = lazy(() => import("./pages/Login"))
const Profile = lazy(() => import("./pages/Profile"))
const Logout = lazy(() => import("./pages/Logout"))
const SignUp = lazy(() => import("./pages/Singup"))
const CreatePoll = lazy(() => import("./pages/CreatePoll"))
const Poll = lazy(() => import("./pages/Poll"))

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
    path: "/poll/:pollId",
    element: <Poll />
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
    path: "/profile/:username",
    element: <Profile />,
  },
  {
    path: "/signup",
    element: <SignUp />,
  },
  {
    path: "/create",
    element: <CreatePoll />,
  },
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <AuthProvider authType={'cookie'}
                authName={'_auth'}
                refresh={refreshApi}
                cookieDomain={window.location.hostname}
                cookieSecure={window.location.protocol === "https:"}>
    <ToastContainer />
    <Navbar />
    <Suspense>
      <RouterProvider router={router} />
    </Suspense>
  </AuthProvider>,
)
