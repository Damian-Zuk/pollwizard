import { useState } from 'react';

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
    options: PollOption[]
}

function PollForm(props: PollFormProps) {
    const [showResults, setShowResults] = useState(false)
    
    let totalVotes = 0
    props.options.map((option) => {
        totalVotes += option.votes
    })

    return (
        <div className="mb-5">
            <form>
                <div className="form-group">
                    <h3>{props.title}</h3>
                    <p className="poll-info">Created by {props.created_by} at {props.created_at}, total votes: {totalVotes}</p>
                    {props.options.map((option) => (
                        <div className="form-check mb-2">
                            <input type="radio" className="form-check-input" name="pollOption" id={`option_${option.id}`} />
                            <label className="form-check-label" htmlFor={`option_${option.id}`}>
                                {option.value} 
                                &nbsp;
                                {showResults && <span className="light-green">{(option.votes / totalVotes * 100).toFixed(2)}%</span>}
                                &nbsp;
                                {showResults && <span className="light-yellow">({option.votes})</span>}
                            </label>
                        </div>
                    ))}
                </div>
            </form>
            <button className="btn btn-success mt-2">Vote</button>
            <button className="btn btn-success mt-2 mx-3" onClick={() => setShowResults(!showResults)}>Show results</button>
        </div>
    );
}

export default PollForm;