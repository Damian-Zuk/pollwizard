import { useParams } from 'react-router-dom';
import PollsContainer from "../components/PollsContainer";

function Poll() {
    const { pollId } = useParams()
    
    return <PollsContainer endpoint={`?poll_id=${pollId}`} />
}

export default Poll;
