import { useParams } from "react-router-dom";
import PollsContainer from '../components/PollsContainer';

function Profile() {
    const { username } = useParams()

    return (
        <>
            <div className="container text-center">
                <h1><b>{username}</b></h1>
                <h3>User profile view</h3>
                <h4 className="mt-5">List of polls</h4>
                <hr />
            </div>
            <PollsContainer endpoint={`user?username=${username}`} />
        </>
    );
}

export default Profile;
