
import PollForm from "../components/PollForm";
import { PollFormProps } from "../components/PollForm";
import { useState, useEffect } from 'react';
import { useAuthHeader } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import axios from "axios";
import { toast } from 'react-toastify'

function PollsContainer(props: {endpoint: string}) {
    const [data, setData] = useState<PollFormProps[]>([]);

    const isAuthenticated = useIsAuthenticated()
    const authHeader = useAuthHeader()

    const fetchData = async () : Promise<PollFormProps[]> => {
        try {
            const pollsResponse = await axios.get(`polls/${props.endpoint}`)

            if (isAuthenticated()) {
                const votesResponse = await axios.get(`polls/my-votes`, {
                    params: {
                        poll_ids: pollsResponse.data.map((entry: PollFormProps) => entry.id).join(',')
                    },
                    headers: { Authorization: authHeader() }
                })
                return pollsResponse.data.map((entry: PollFormProps) => ({
                    ...entry,
                    _voted_for: votesResponse.data[entry.id]
                }))
            } else {
                return pollsResponse.data
            }
        } catch (err: any) {
            toast.error(err.response!.data.detail, {
                position: "top-center",
                autoClose: 2000,
            });
        }
        return []
    };

    useEffect(() => {
        fetchData().then((data) => setData(data))
    }, [props.endpoint])

    return (
        <div className="container poll-forms-container">
        {
            data.map((entry: PollFormProps) => (
                <PollForm 
                    {...entry} 
                    _is_single_poll_view={props.endpoint.startsWith('?')} 
                    key={entry.id}
                />
            ))
        }
        </div>
    );
}

export default PollsContainer;