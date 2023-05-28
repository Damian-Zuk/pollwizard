import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import { useAuthHeader } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import PollForm, { PollFormProps } from "../components/PollForm"

function Poll() {
    const { pollId } = useParams()

    const isAuthenticated = useIsAuthenticated()
    const authHeader = useAuthHeader()
    const header = {headers: isAuthenticated() ? {Authorization: authHeader()} : {}}
    const [notFound, setNotFound] = useState(false)

    const [data, setData] = useState<PollFormProps>({
        id: 0,
        title: "",
        created_by: "",
        created_at: "",
        voted_for: -1,
        options: [],
        _is_poll_page: false
    });

    useEffect(() => {
        axios
        .get(`http://localhost:8000/polls/?poll_id=${pollId}`, header)
        .then((response) => {
            setData(response.data[0]);
        })
        .catch((err) => {
            if (err.response.status == 404)
                setNotFound(true)
            else 
                console.log(err)
        });
    }, []);

    if (notFound)
        return (
            <div className="container vh-100 text-center">
                <h1>Error 404</h1>
                <h3>Poll not found</h3>
            </div>
        );

    return (
        <div className="container poll-forms-container">
            <PollForm {...data} _is_poll_page={true}/>
        </div>
    );
}

export default Poll;
