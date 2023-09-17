import axios from 'axios';
import { useState } from 'react';
import { useAuthHeader, useAuthUser } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify'
import { confirmAlert } from 'react-confirm-alert';

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
    options: PollOption[],
    _voted_for: number,
    _is_single_poll_view: boolean
}

function PollForm(props: PollFormProps) {
    const [showResults, setShowResults] = useState(false)
    const [selectedOption, setSelectedOption] = useState(-1)
    const [voted, setVoted] = useState(false)
    const [deleted, setDeleted] = useState(false)

    const authHeader = useAuthHeader()
    const isAuthenticated = useIsAuthenticated()
    const navigate = useNavigate();
    const user = useAuthUser()

    if (deleted)
        return (<></>)
    
    const onVote = async (event: any) => {
        event.preventDefault()

        if (!isAuthenticated()) {
            navigate('/login')
            return
        }
        if (selectedOption == -1)
            return
        
        try {
            await axios.post(`polls/vote?option_id=${selectedOption}`, {}, {
                headers: { Authorization: authHeader() }
            })
            for (let i = 0; i < props.options.length; i++) {
                if (props.options[i].id == selectedOption) {
                    props.options[i].votes++
                    setShowResults(true)
                    setVoted(true)
                    break
                }
            }
            toast.success(`Voted for ${props.created_by}'s poll`, {
                position: "top-center",
                autoClose: 2000,
                hideProgressBar: true
            });
        } catch (err: any) {
            toast.error(err.response!.data.detail, {
                position: "top-center",
                autoClose: 2000,
            });
        }
    }

    const onDelete = async (pollID: number, isPollPage: boolean) => {
        try {
            const response = await axios.delete(`polls/?poll_id=${pollID}`, {
                headers: { Authorization: authHeader() }
            })
            toast.success(response.data.detail, {
                position: "top-center",
                autoClose: 1000,
                hideProgressBar: true
            });
            if (isPollPage)
                navigate("/")
            setDeleted(true)
        } catch (err: any) {
            toast.error(err.response!.data.detail, {
                position: "top-center",
                autoClose: 2000,
                hideProgressBar: true
            });
        }
    }

    const showDeleteConfirmation = (e: any, pollID: number, isPollPage: boolean) => {
        e.preventDefault()
        confirmAlert({
            title: "Confirmation",
            message: "Are you sure you want to delete this poll?",
            buttons: [
              {
                label: "Delete",
                onClick: () => onDelete(pollID, isPollPage)
              },
              {
                label: "Cancel",
                onClick: () => {}
              }
            ]
          });
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
                        {props._is_single_poll_view 
                        ? <h3>{props.title}</h3>
                        : <a href={`/poll/${props.id}`}><h3>{props.title}</h3></a>}
                    </div>

                    {props.options.map((option) => (
                        <div className="form-check mb-2" key={`option_${option.id}`}>
                            <input 
                                type="radio" 
                                className="form-check-input" 
                                name="pollOption" 
                                id={`option_${option.id}`}
                                value={option.value} 
                                disabled={props._voted_for >= 0 || voted}
                                checked={props._voted_for == option.id || selectedOption == option.id}
                                onChange={() => setSelectedOption(option.id)}
                            />

                            <label className="form-check-label d-block" htmlFor={`option_${option.id}`}>
                                { props._voted_for == option.id || (voted && selectedOption == option.id)
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
                    
                    { user()?.name == props.created_by &&
                        <button className="btn btn-danger"
                            onClick={(e) => showDeleteConfirmation(e, props.id, props._is_single_poll_view)}>
                            <i className="fa-solid fa-trash"></i>
                        </button>
                    }

                    <button className="btn btn-success mx-3" 
                        onClick={(e) => {e.preventDefault(); setShowResults(!showResults)}}>
                            {showResults ? `Hide results` : `View results` }
                    </button>

                    { props._voted_for !== undefined && (props._voted_for !== -1 || voted)
                    ? <div className="d-inline-block align-middle mx-2"><i className="fa-solid fa-check"></i> Voted </div> 
                    :
                        <button className="btn btn-success" 
                            disabled={props._voted_for >= 0}
                            onClick={onVote}>
                            <i className="fa-solid fa-check"></i> Vote
                        </button>
                    }

                </div>
            </div>
        </form>
    );
}

export default PollForm;
