import { useIsAuthenticated } from 'react-auth-kit';
import { useSignOut } from 'react-auth-kit'
import { Navigate } from "react-router-dom";

function Logout()
{
    const isAuthenticated = useIsAuthenticated()
    const signOut = useSignOut()

    if (isAuthenticated())
        signOut()

    return <Navigate to="/" />;
}

export default Logout;
