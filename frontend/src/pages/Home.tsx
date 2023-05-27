import PollForm from "../components/PollForm";
import { PollFormProps } from "../components/PollForm";
import { useState, useEffect } from 'react';
import { useAuthHeader } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import axios from "axios";

function Home() {
    const [data, setData] = useState<PollFormProps[]>([]);

    const isAuthenticated = useIsAuthenticated()
    const authHeader = useAuthHeader()
    const header = {headers: isAuthenticated() ? {Authorization: authHeader()} : {}}

    useEffect(() => {
        axios
            .get(`http://localhost:8000/polls/all`, header)
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
                <PollForm {...entry}  _title_is_link={true} key={entry.id}/>
            ))}
        </div>
        
    );
}

export default Home;
