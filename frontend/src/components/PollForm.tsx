import axios from 'axios';
import { useState } from 'react';
import { useAuthHeader } from 'react-auth-kit'
import { toast } from 'react-toastify'

export interface PollOption
{
    id: number
    value: string,
    votes: number
}

export interface PollFormProps
{
    id: number,
    title: string,
    created_by: string,
    created_at: string,
    voted_for: number,
    options: PollOption[],
    _title_is_link: boolean
}

function PollForm(props: PollFormProps) {
    const [showResults, setShowResults] = useState(false)
    const [selectedOption, setSelectedOption] = useState(-1)
    const [voted, setVoted] = useState(false)
    const authHeader = useAuthHeader()
    
    const onVote = async (event: any) => {
        event.preventDefault()
        if (selectedOption == -1)
            return
        try 
        {
            await axios.post(`http://localhost:8000/polls/vote?optionID=${selectedOption}`, {},
                {
                    headers: { Authorization: authHeader() }
                }
            ).then((response) => {
                if ("error" in response.data)
                {
                    toast.error(response.data.error, {
                        position: "top-center",
                        autoClose: 2000,
                    });
                }
                else
                {
                    let index = 0;
                    for (var option of props.options.values()) {
                        if (option.id == selectedOption) {
                            props.options[index].votes++
                            setShowResults(true)
                            setVoted(true)
                            break
                        }
                        index++
                    }
                    toast.success(`Voted for ${props.created_by}'s poll!`, {
                        position: "top-center",
                        autoClose: 2000,
                    });
                }
            })
            
        } catch(err) {
            console.log("Error: ", err)
        }
    }

    let totalVotes = 0
    props.options.map((option) => {
        totalVotes += option.votes
    })

    return (
        <div className="mb-5">
            <form className="poll-form">
                <div className="form-group">
                    {props._title_is_link 
                    ? <a href={`/poll/${props.id}`}><h3>{props.title}</h3></a>
                    : <h3>{props.title}</h3>}
                    <p className="poll-info">Created by {props.created_by} at {props.created_at}, total votes: {totalVotes}</p>
                    {props.options.map((option) => (
                        <div className="form-check mb-2" key={`option_${option.id}`}>
                            <input type="radio" className="form-check-input" name="pollOption" 
                                id={`option_${option.id}`}
                                disabled={props.voted_for != -1}
                                checked={props.voted_for == option.id || selectedOption == option.id}
                                onChange={() => setSelectedOption(option.id)}
                                value={option.value} />
                            <label className="form-check-label" htmlFor={`option_${option.id}`}>
                                { props.voted_for == option.id ? <span className="light-green">{option.value}</span> : option.value} 
                                &nbsp;
                                {showResults && <span className="light-green">{totalVotes > 0 ? (option.votes / totalVotes * 100).toFixed(2) : 0}%</span>}
                                &nbsp;
                                {showResults && <span className="light-yellow">({option.votes})</span>}
                            </label>
                        </div>
                    ))}
                </div>
                <div>
                    { props.voted_for != -1 || voted
                    ? <div className="d-inline-block align-middle"><i className="fa-solid fa-check"></i> Voted </div> 
                    :
                        <button className="btn btn-success mt-2" 
                            disabled={props.voted_for != -1}
                            onClick={(e) => onVote(e)}>
                            Vote
                        </button>
                    }
                    <button className="btn btn-success mt-2 mx-3" 
                        onClick={(e) => {e.preventDefault(); setShowResults(!showResults)}}>
                            Show results
                    </button>
                </div>

            </form>
        </div>
    );
}

export default PollForm;
