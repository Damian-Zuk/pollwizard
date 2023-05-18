import { useIsAuthenticated } from 'react-auth-kit';
import '../styles/main.css'

function Navbar() {
    const isAuthenticated = useIsAuthenticated()

    return (
        <>
        <nav className="navbar navbar-expand-lg bg-success navbar-dark mb-5">
        <div className="container-fluid">

            <a className="navbar-brand mx-5" href="/">Poll<span className="light-green">Wizard</span></a>
            <button className="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <i className="fas fa-bars"></i>
            </button>

            <div className="collapse navbar-collapse" id="navbarSupportedContent">

            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                <li className="nav-item mx-2">
                <a className="nav-link" href="/">Home</a>
                </li>
                <li className="nav-item mx-2">
                <a className="nav-link" href="/create">Create poll</a>
                </li>
            </ul>

            <ul className="navbar-nav d-flex flex-row me-5">
                <li className="nav-item me-3 me-lg-0 mx-2">
                { isAuthenticated() 
                ? <a className="nav-link" href="/profile">My profile</a>
                : <a className="nav-link" href="/login">Sign in</a> }
                </li>

                <li className="nav-item me-3 me-lg-0 mx-2">
                { isAuthenticated() 
                ? <a className="nav-link" href="/logout">Log out</a>
                : <a className="nav-link" href="/signup">Sign up</a> }
                </li>
            </ul>

            </div>
        </div>
        </nav>
        </>
    );
}

export default Navbar;