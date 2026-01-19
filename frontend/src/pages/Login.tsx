import { useState } from 'react';
import { useSignIn } from 'react-auth-kit'
import { Navigate } from "react-router-dom";
import { useIsAuthenticated } from 'react-auth-kit';
import { toast } from 'react-toastify'
import axios from "axios";

function Login() 
{
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    
    const signIn = useSignIn();
    const isAuthenticated = useIsAuthenticated()

    if (isAuthenticated())
        return <Navigate to="/" />;

    const onSubmit = async () => {

        if (!email.length || !password.length)
            return;

        try {
            const response = await axios.post("users/login", {
                "email": email,
                "password": password
            })
            try {
                const userDataResponse = await axios.get("users", {
                    headers: { Authorization: `Bearer ${response.data.access}` }
                })
                signIn({
                    tokenType: "Bearer",
                    token: response.data.access,
                    expiresIn: 600,
                    refreshToken: response.data.refresh,
                    refreshTokenExpireIn: 86400,
                    authState: { 
                        email: userDataResponse.data.email,
                        name: userDataResponse.data.name,
                    }
                })
                toast.success(`Welcome back, ${userDataResponse.data.name}!`, {
                    position: "top-center",
                    autoClose: 2000,
                })
            } catch (err) {
                console.log(err)
                toast.error("Unexpected error occured during fetching user data", {
                    position: "top-center",
                    autoClose: 2000,
                });
            }
        } catch (err: any) {
            setError("Invalid email address or password!")
            if (err.response && err.response.status === 429) {
                toast.error("Oops! It seems you've exceeded the login attempt limit. Please wait a moment and try again later.", {
                    position: "top-center",
                    autoClose: 2000,
                });
            }
        }
    }

    const onKeyPress = (e: any) => {
        if (e.keyCode === 13)
            onSubmit()
    }

    return (
        <section className="vh-100">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 mx-auto">
                        <div className="d-flex align-items-center mt-5">

                            <form className="login-form mx-auto">

                                <h3 className="fw-normal mb-3 pb-3 login-header">Sign In</h3>
                                <p className="error-color">{error}</p>

                                <div className="form-outline mb-4">
                                    <input 
                                        type="email"
                                        id="loginEmail" 
                                        className="form-control form-control-lg"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        placeholder="Email" />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="password" 
                                        id="loginPassword" 
                                        className="form-control form-control-lg"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        onKeyDownCapture={onKeyPress}
                                        placeholder="Password"/>
                                </div>

                                <div className="pt-1 mb-4">
                                    <button className="btn btn-success btn-lg btn-block" type="button" onClick={() => onSubmit()}>Sign in</button>
                                </div>

                                <div className="text-center">
                                    <p>You do not have an account? <a href="/signup">Sign up here</a></p>
                                </div>

                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Login;
