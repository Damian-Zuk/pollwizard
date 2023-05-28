
import PollForm from "../components/PollForm";
import { PollFormProps } from "../components/PollForm";
import { useState, useEffect } from 'react';
import { useAuthHeader } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import axios from "axios";

function PollsContainer(props: {endpoint: string}) {
    const [data, setData] = useState<PollFormProps[]>([]);

    const isAuthenticated = useIsAuthenticated()
    const authHeader = useAuthHeader()

    useEffect(() => {
        axios
            .get(`http://localhost:8000/polls/${props.endpoint}`, {
                headers: isAuthenticated() ? {Authorization: authHeader()} : {}
            })
            .then((response) => {
                setData(response.data);
            })
            .catch((error) => {
                console.error(error);
            });
    }, []);

    return (
        <div className="container poll-forms-container">
            {data.map((entry: PollFormProps) => (
                <PollForm {...entry}  _is_poll_page={false} key={entry.id}/>
            ))}
        </div>
    );
}

export default PollsContainer;