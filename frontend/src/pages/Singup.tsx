import { useRef, useState } from 'react';
import { Navigate } from "react-router-dom";
import { useIsAuthenticated } from 'react-auth-kit';
import { useSignIn } from 'react-auth-kit'
import { ToastContainer, toast } from 'react-toastify'
import ReCAPTCHA from 'react-google-recaptcha'
import axios from "axios";
import "../styles/login.css"
import "react-toastify/dist/ReactToastify.css"

interface ErrorType {
    email: string;
    name: string;
    password: string;
    passwordRepeat: string;
    captcha: string;
  }

function SignUp() {
    const [email, setEmail] = useState("")
    const [name, setName] = useState("")
    const [password, setPassword] = useState("")
    const [passwordRepeat, setPasswordRepeat] = useState("")
    const [captchaIsDone, setCaptchaIsDone] = useState(false)
    const [signUpSuccess, setSignUpSuccess] = useState(false)
    const [error, setError] = useState<ErrorType>({email: "", name: "", password: "", passwordRepeat: "", captcha: ""})
    
    const isAuthenticated = useIsAuthenticated()
    const signIn = useSignIn();

    if (isAuthenticated())
        return <Navigate to="/" />;

    const onCaptchaChange = () => {
        setCaptchaIsDone(true)
        setError({...error, captcha: ""})
        console.log("Captcha change")
    }

    const validateEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    const onSubmit = async () => {

        const errorReset = {
            email:          email.length          ? "" : "This field must not be empty!",
            name:           name.length           ? "" : "This field must not be empty!",
            password:       password.length       ? "" : "This field must not be empty!",
            passwordRepeat: passwordRepeat.length ? "" : "This field must not be empty!",
            captcha: captchaIsDone ? "" : "Please complete the CAPTCHA verification to proceed.",
        }

        if (email.length && !validateEmail(email))
            errorReset.email = "This is not valid email address!"
        
        if (password != passwordRepeat)
            errorReset.passwordRepeat = "Passwords do not match!"
        
        setError(errorReset)

        for (const msg of Object.entries(errorReset).values())
            if (msg[1].length) 
                return;
        try 
        {
            const res = await axios.post(
                "http://localhost:8000/users/signup",
                {
                    email: email,
                    name: name,
                    password: password
                }
            )

            if ("errors" in res.data)
            {
                for (const [e, message] of Object.entries(res.data["errors"]))
                {
                    setError((prevError) => ({ ...prevError, [e]: message }));
                }
                return;
            }

            setSignUpSuccess(true)
            toast.success("Account successfully created! Returning to homepage ...", {
                position: "top-center",
                autoClose: 3000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "light",
                onClose: () => {
                    signIn(
                        {
                            token: res.data.token,
                            expiresIn: 3600,
                            tokenType: "Bearer",
                            authState: { email: email, name: res.data.userName }
                        }
                    )
                }
            });

        } catch(err) {
            toast.error("Unexpected error occured!", {
                position: "top-center",
                autoClose: 2000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "light",
            });
            console.log("Error: ", err)
        }
    }

    const userDataInput = (fieldName: string, placeholder: string, value: string, setFunc: React.Dispatch<React.SetStateAction<string>>) => {
        const errorMessage = error[fieldName as keyof ErrorType]
        return (
            <>
                <div className="mb-1">{placeholder}</div>
                <div className={errorMessage.length > 0 ? "form-outline" : "form-outline mb-4"} >
                    <input 
                        type={fieldName.toLowerCase().includes("password") ? "password" : "text"}
                        id={fieldName} 
                        className={errorMessage.length > 0 
                            ? "form-control form-control-lg is-invalid" 
                            : "form-control form-control-lg"}
                        value={value}
                        onChange={(e) => setFunc(e.target.value)}
                        placeholder={placeholder}
                    />
                </div>
                {errorMessage.length > 0 && <div className="error-color">{errorMessage}</div>}
            </>
        );
    }

    return (
        <>
        <ToastContainer />
        <section className="vh-100">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 mx-auto">
                        <div className="d-flex align-items-center h-custom-2 ms-xl-4 mt-4">

                            <form className="login-form mx-auto">

                                <h3 className="fw-normal mb-2 pb-3 login-header">Create account</h3>

                                {userDataInput("name", "Name", name, setName)}
                                {userDataInput("email", "Email", email, setEmail)}
                                {userDataInput("password", "Password", password, setPassword)}
                                {userDataInput("passwordRepeat", "Repeat password", passwordRepeat, setPasswordRepeat)}

                                <ReCAPTCHA
                                    sitekey="6LfcGCkmAAAAAKXH1Jzi9Gas2vQX7FXRGHCfHa0o"
                                    onChange={onCaptchaChange}
                                    className="recaptcha-from mt-5"
                                />
                                {error.captcha.length > 0 && <div className="error-color mt-1">{error.captcha}</div>}

                                <div className={error.captcha.length > 0 ? "pt-1 mt-3" : "pt-1 mt-5" }>
                                    <button 
                                        className="btn btn-success btn-lg btn-block" 
                                        type="button" 
                                        onClick={() => onSubmit()}
                                        disabled={signUpSuccess}>
                                        Sign up
                                    </button>
                                </div>

                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        </>
    );
}

export default SignUp;