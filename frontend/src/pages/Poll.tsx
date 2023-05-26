import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import { useAuthHeader } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import PollForm, { PollFormProps } from "../components/PollForm"

function Poll(){
    const { pollId } = useParams()

    const isAuth = useIsAuthenticated()
    const authHeader = useAuthHeader()

    const header = isAuth() ? {Authorization: authHeader()} : {}
    const endpoint = isAuth() ? "one-auth" : "one"

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
        .get(`http://localhost:8000/polls/${endpoint}?poll_id=${pollId}`, {headers: header})
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