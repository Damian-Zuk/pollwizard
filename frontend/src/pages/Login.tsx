import { useRef, useState } from 'react';
import { useSignIn } from 'react-auth-kit'
import { Navigate } from "react-router-dom";
import { useIsAuthenticated } from 'react-auth-kit';
import axios from "axios";
import "../styles/login.css"

function Login() {
    const emailRef = useRef<HTMLInputElement>(null)
    const passwordRef = useRef<HTMLInputElement>(null)
    const [error, setError] = useState("")
    const signIn = useSignIn();
    const isAuthenticated = useIsAuthenticated()

    if (isAuthenticated())
        return <Navigate to="/" />;

    const onSubmit = async () => {

        if (!emailRef.current?.value.length || !passwordRef.current?.value.length)
            return;

        try 
        {
            const res = await axios.post(
                "http://localhost:8000/users/login",
                {
                    "email": emailRef.current.value,
                    "password": passwordRef.current.value
                }
            )

            if ("error" in res.data)
                setError("Invalid email address or password!")
            else
            {
                signIn(
                    {
                        token: res.data.token,
                        expiresIn: 3600,
                        tokenType: "Bearer",
                        authState: { email: emailRef.current.value, name: res.data.userName }
                    }
                )
            }
        } catch(err) {
            setError("Invalid email address or password!")
            console.log("Error: ", err)
        }
    }

    return (
        <section className="vh-100">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 mx-auto">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">

                            <form className="login-form mx-auto">

                                <h3 className="fw-normal mb-3 pb-3 login-header">Sign In</h3>
                                <p className="error-color">{error}</p>

                                <div className="form-outline mb-4">
                                    <input 
                                        type="email"
                                        id="loginEmail" 
                                        className="form-control form-control-lg"
                                        ref={emailRef}
                                        placeholder="Email" />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="password" 
                                        id="loginPassword" 
                                        className="form-control form-control-lg"
                                        ref={passwordRef}
                                        placeholder="Password"/>
                                </div>

                                <div className="pt-1 mb-4">
                                    <button className="btn btn-success btn-lg btn-block" type="button" onClick={() => onSubmit()}>Sign in</button>
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