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

    const [data, setData] = useState<PollFormProps>({
        id: 0,
        title: "",
        created_by: "",
        created_at: "",
        voted_for: -1,
        options: [],
        _title_is_link: false
    });

    useEffect(() => {
        axios
        .get(`http://localhost:8000/polls/?poll_id=${pollId}`, header)
        .then((response) => {
            setData(response.data[0]);
        })
        .catch((error) => {
            console.error(error);
        });
    }, []);

    return (
        <div className="vh-100 container">
            <div className="row">
                <div className="col-sm-6 mx-auto">
                    <PollForm {...data} _title_is_link={false}/>
                </div>
            </div>
        </div>
    );
}

export default Poll;
