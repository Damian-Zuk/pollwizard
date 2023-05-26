import { useAuthUser } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import { Navigate } from "react-router-dom";

function Profile()
{
    const isAuthenticated = useIsAuthenticated()
    const auth = useAuthUser()

    if (!isAuthenticated())
        return <Navigate to="/" />;

    return (
        <div className="container">
            <h1>Hello {auth()?.name}!</h1>
        </div>
    );
}

export default Profile;
