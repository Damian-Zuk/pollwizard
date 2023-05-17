import "../styles/login.css"

function Login() {

    return (
        <section className="vh-100">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 mx-auto">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">

                            <form className="login-form mx-auto">

                                <h3 className="fw-normal mb-3 pb-3 login-header">Log in</h3>

                                <div className="form-outline mb-4">
                                    <input type="email" id="loginEmail" className="form-control form-control-lg" placeholder="Email address" />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="password" id="loginPassword" className="form-control form-control-lg" placeholder="Password"/>
                                </div>

                                <div className="pt-1 mb-4">
                                    <button className="btn btn-success btn-lg btn-block" type="button">Login</button>
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