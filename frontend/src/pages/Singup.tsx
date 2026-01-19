import { useState } from 'react';
import { Navigate } from "react-router-dom";
import { useIsAuthenticated } from 'react-auth-kit';
import { useSignIn } from 'react-auth-kit'
import { toast } from 'react-toastify'
import ReCAPTCHA from 'react-google-recaptcha'
import axios from "axios";

interface ErrorType {
    email: string;
    name: string;
    pass: string;
    repass: string;
    captcha: string;
  }

function SignUp() {
    const [email, setEmail] = useState("")
    const [name, setName] = useState("")
    const [pass, setPassword] = useState("")
    const [repass, setPasswordRepeat] = useState("")
    const [captchaIsDone, setCaptchaIsDone] = useState(false)
    const [error, setError] = useState<ErrorType>({email: "", name: "", pass: "", repass: "", captcha: ""})
    
    const isAuthenticated = useIsAuthenticated()
    const signIn = useSignIn();

    if (isAuthenticated())
        return <Navigate to="/" />;

    const onCaptchaChange = () => {
        setCaptchaIsDone(true)
        if (error.captcha.length)
            setError({...error, captcha: ""})
    }

    const validateEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    const onSubmit = async () => {

        const errorReset = {
            email:   email.length  ? "" : "This field cannot be empty!",
            name:    name.length   ? "" : "This field cannot be empty!",
            pass:    pass.length   ? "" : "This field cannot be empty!",
            repass:  repass.length ? "" : "This field cannot be empty!",
            captcha: captchaIsDone ? "" : "Please complete the CAPTCHA verification to proceed.",
        }

        if (email.length && !validateEmail(email))
            errorReset.email = "This is not valid email address!"
        
        if (pass != repass)
            errorReset.repass = "The passwords are not the same!"
        
        setError(errorReset)

        for (const msg of Object.entries(errorReset).values())
            if (msg[1].length) 
                return;

        try {
            const response = await axios.post("users/signup", {
                email: email,
                name: name,
                password: pass,
            })
            signIn({
                tokenType: "Bearer",
                token: response.data.access,
                expiresIn: 600,
                refreshToken: response.data.refresh,
                refreshTokenExpireIn: 86400,
                authState: { email: email, name: name }
            })
            toast.success("You have registered sucessfully", {
                position: "top-center",
                autoClose: 5000,
            })
        } catch (err: any) {
            for (const [e, message] of Object.entries(err.response.data.detail!.errors))
                setError((prevError) => ({ ...prevError, [e]: message }));
        }
    }

    const userDataInput = (fieldName: string, placeholder: string, value: string, setFunc: React.Dispatch<React.SetStateAction<string>>) => {
        const errorMessage = error[fieldName as keyof ErrorType]
        return (
            <>
                <div className="mb-1">{placeholder}</div>
                <div className={errorMessage.length > 0 ? "form-outline" : "form-outline mb-4"} >
                    <input 
                        type={fieldName.toLowerCase().includes("pass") ? "password" : "text"}
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
        <section className="vh-100">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 mx-auto">
                        <div className="d-flex align-items-center">

                            <form className="login-form mx-auto">

                                <h3 className="fw-normal mb-2 pb-3 login-header">Create account</h3>

                                {userDataInput("name", "Name", name, setName)}
                                {userDataInput("email", "Email", email, setEmail)}
                                {userDataInput("pass", "Password", pass, setPassword)}
                                {userDataInput("repass", "Repeat password", repass, setPasswordRepeat)}
                                
                                <p className="password-disclaimer mx-auto">
                                    Passwords must be at least 8 characters long and include at least one uppercase and lowercase letter, one digit, and one special character.
                                </p>

                                <ReCAPTCHA
                                    sitekey="6LfcGCkmAAAAAKXH1Jzi9Gas2vQX7FXRGHCfHa0o"
                                    onChange={onCaptchaChange}
                                    className="recaptcha-from mt-4"
                                />
                                {error.captcha.length > 0 && <div className="error-color mt-1">{error.captcha}</div>}

                                <div className={error.captcha.length > 0 ? "pt-1 mt-3" : "pt-1 mt-5" }>
                                    <button 
                                        className="btn btn-success btn-lg btn-block" 
                                        type="button" 
                                        onClick={() => onSubmit()}>
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
