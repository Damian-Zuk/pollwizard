import { useIsAuthenticated } from 'react-auth-kit';
import { useSignOut } from 'react-auth-kit'
import { Navigate } from "react-router-dom";
import { useAuthHeader } from 'react-auth-kit'
import { toast } from 'react-toastify'
import axios from "axios";

function Logout()
{
    const isAuthenticated = useIsAuthenticated()
    const signOut = useSignOut()
    const authHeader = useAuthHeader()

    if (isAuthenticated()) {
        try {
            axios.post(`/logout`, { 
                headers: { Authorization: authHeader() }
            })
            toast.success("Logout successful. Have a great day!", {
                position: "top-center",
                autoClose: 2000,
            })
        } catch (err: any) {
            toast.error(err.response!.data.detail, {
                position: "top-center",
                autoClose: 2000,
            })
        }
        signOut()
    }

    return <Navigate to="/" />;
}

export default Logout;
