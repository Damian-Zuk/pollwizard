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
                            //setVoted(true)
                            break
                        }
                        index++
                    }
                    toast.success(`Voted for ${props.created_by}'s poll`, {
                        position: "top-center",
                        autoClose: 2000,
                        hideProgressBar: true
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
        <form className="poll-form">
            <div className="row">
                <div className="col-md-8">
                    <div className="poll-title">
                        {props._title_is_link 
                        ? <a href={`/poll/${props.id}`}><h3>{props.title}</h3></a>
                        : <h3>{props.title}</h3>}
                    </div>

                    {props.options.map((option) => (
                        <div className="form-check mb-2" key={`option_${option.id}`}>
                            <input 
                                type="radio" 
                                className="form-check-input" 
                                name="pollOption" 
                                id={`option_${option.id}`}
                                value={option.value} 
                                disabled={props.voted_for != -1 || voted}
                                checked={props.voted_for == option.id || selectedOption == option.id}
                                onChange={() => setSelectedOption(option.id)}
                            />

                            <label className="form-check-label d-block" htmlFor={`option_${option.id}`}>
                                { props.voted_for == option.id || (voted && selectedOption == option.id)
                                ? <span className="light-green"><b>{option.value}</b></span> 
                                : option.value
                                }
                                &nbsp;
                                {showResults && <span className="light-yellow">({option.votes})</span>}
                            </label>
                            
                            {showResults &&
                                <>
                                    <div className="pollBarContainer">
                                        <div className="pollBar" style={{width: `${totalVotes > 0 ? (option.votes / totalVotes * 100).toFixed(0) : 0}%`}}></div>
                                    </div>
                                    <div className="barPercent">
                                        {totalVotes > 0 ? (option.votes / totalVotes * 100).toFixed(1) : 0} %
                                    </div>
                                </>
                            }
                        </div>
                    ))}
                </div>

                <div className="col-md-4">
                    <div className="poll-info">
                        <div>
                            <a href={`/profile/${props.created_by}`}>{props.created_by}</a> @ {props.created_at.replace("T", " ")}
                        </div>
                        <div>
                            {totalVotes} Votes
                        </div>
                    </div>
                </div>
            </div>

            <div className="poll-form-buttons-container">
                <div className="poll-form-buttons-block">

                    <button className="btn btn-success mx-3" 
                        onClick={(e) => {e.preventDefault(); setShowResults(!showResults)}}>
                            Show results
                    </button>

                    { props.voted_for != -1 || voted
                    ? <div className="d-inline-block align-middle"><i className="fa-solid fa-check"></i> Voted </div> 
                    :
                        <button className="btn btn-success" 
                            disabled={props.voted_for != -1}
                            onClick={(e) => onVote(e)}>
                            Vote
                        </button>
                    }

                </div>
            </div>
        </form>
    );
}

export default PollForm;
