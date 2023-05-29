import 'bootstrap/dist/css/bootstrap.css'
import "react-toastify/dist/ReactToastify.css"
import 'react-confirm-alert/src/react-confirm-alert.css';
import "./styles/main.css"

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { AuthProvider } from 'react-auth-kit';
import { ToastContainer } from 'react-toastify';

import refreshApi from './auth/RefreshApi';

import Home from './pages/Home'
import Login from './pages/Login'
import Profile from './pages/Profile'
import Logout from './pages/Logout';
import SignUp from './pages/Singup';
import CreatePoll from './pages/CreatePoll';
import Poll from './pages/Poll';

import Navbar from './components/Navbar'


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

const App = () => (
  <AuthProvider authType={'cookie'}
                authName={'_auth'}
                refresh={refreshApi}
                cookieDomain={window.location.hostname}
                cookieSecure={window.location.protocol === "https:"}>
    <ToastContainer />
    <Navbar />
    <RouterProvider router={router} />
  </AuthProvider>
);

export default App;
