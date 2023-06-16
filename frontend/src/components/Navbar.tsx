import { useIsAuthenticated } from 'react-auth-kit';
import { useAuthUser } from 'react-auth-kit'

function Navbar() {
    const isAuthenticated = useIsAuthenticated()
    const user = useAuthUser()

    return (
        <>
        <nav className="navbar navbar-expand-lg navbar-dark mb-5">
        <div className="container-fluid">

            <a className="navbar-brand mx-5" href="/">Poll<span className="light-green">Wizard</span></a>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                 <i className="fas fa-bars"></i>
            </button>


            <div className="collapse navbar-collapse" id="navbarSupportedContent">

            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                <li className="nav-item mx-2">
                <a className="nav-link" href="/"><i className="fa-solid fa-house"></i> Home</a>
                </li>
                <li className="nav-item mx-2">
                <a className="nav-link" href="/create"><i className="fa-solid fa-plus"></i> Create poll</a>
                </li>
            </ul>

            <ul className="navbar-nav d-flex flex-row me-5">
                <li className="nav-item me-3 me-lg-0 mx-2">
                { isAuthenticated() 
                ? <a className="nav-link" href={`/profile/${user()?.name}`}><i className="fa-solid fa-user"></i> My profile</a>
                : <a className="nav-link" href="/login"><i className="fa-solid fa-right-to-bracket"></i> Sign in</a> }
                </li>

                <li className="nav-item me-3 me-lg-0 mx-3">
                { isAuthenticated() && <a className="nav-link" href="/logout"><i className="fa-solid fa-right-from-bracket"></i> Log out</a> }
                </li>
            </ul>

            </div>
        </div>
        </nav>
        </>
    );
}

export default Navbar;
