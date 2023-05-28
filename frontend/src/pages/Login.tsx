import { useRef, useState } from 'react';
import { useSignIn } from 'react-auth-kit'
import { Navigate } from "react-router-dom";
import { useIsAuthenticated } from 'react-auth-kit';
import { toast } from 'react-toastify'
import axios from "axios";

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

        try {
            const response = await axios.post("http://localhost:8000/users/login",
            {
                "email": emailRef.current.value,
                "password": passwordRef.current.value
            })
            if ("error" in response.data)
                setError("Invalid email address or password!")
            else
            {
                signIn({
                    token: response.data.token,
                    expiresIn: 3600,
                    tokenType: "Bearer",
                    authState: { email: emailRef.current!.value, name: response.data.userName }
                })
            }
        } catch (err: any) {
            if (err.response!.status == 422)
                setError("Invalid email address or password!")
            else 
                toast.error(err.response!.data.detail, {
                    position: "top-center",
                    autoClose: 2000,
                });
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
