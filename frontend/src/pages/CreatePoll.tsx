import { useState } from "react"
import { useIsAuthenticated } from 'react-auth-kit';
import { useAuthHeader } from 'react-auth-kit'
import { Navigate } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { toast } from 'react-toastify'
import axios from "axios";

function CreatePoll() {

    const [optionCount, setOptionCount] = useState(2)
    const [pollTitle, setPollTitle] = useState("")
    const [optionValues, setOptionValues] = useState<string[]>(["", ""])
    
    const isAuthenticated = useIsAuthenticated()
    const authHeader = useAuthHeader()
    const navigate = useNavigate()

    if (!isAuthenticated())
        return <Navigate to="/login" />;

    const onSubmit = async () => {
        try {
            const response = await axios.post("polls",
            {
                title: pollTitle,
                options: optionValues
            },
            {
                headers: { Authorization: authHeader() }
            })
            toast.success(`The poll has been created`, {
                position: "top-center",
                autoClose: 1000,
                hideProgressBar: true
            });
            navigate(`/poll/${response.data.id}`)

        } catch (err: any) {
            toast.error(err.response!.data.detail, {
                position: "top-center",
                autoClose: 2000,
            });
        }
    }

    const addOption = () => {
        if (optionCount <= 16) {
            setOptionCount(optionCount + 1)
            setOptionValues([...optionValues, ""])
        }
    }

    const removeOption = (e: any, index: number) => {
        e.preventDefault()
        let copy = optionValues
        copy.splice(index, 1)
        setOptionValues(copy)
        setOptionCount(optionCount - 1)
    }

    const renderOptionInputs = () => {
        let optionsJSX = []
        for (let i = 0; i < optionCount; i++) {
            optionsJSX.push(
                <div className={i > 1 ? "mt-1 animate" : "mt-1"}>
                    <div className="mb-1">Option {i + 1}</div>
                    <div className="form-outline mb-2">
                        <input 
                            type="text"
                            id={`pollOption_${i}`}
                            value={optionValues.at(i)}
                            onChange={(e) => {
                                let copy = [...optionValues]
                                copy[i] = e.target.value
                                setOptionValues(copy)
                            }}
                            className={i > 1 ? "form-control add-option-input" : "form-control"}
                            placeholder={`Option ${i + 1}...`}
                        />
                        { i > 1 && <button className="btn btn-danger remove-btn" onClick={(e) => removeOption(e, i)}><i className="fa-solid fa-trash"></i></button> }
                    </div>
                </div>
            );
        }
        return optionsJSX
    }

    let emptyFields = pollTitle.length == 0
    for (const option of optionValues.values()) {
        if (option.length == 0) {
            emptyFields = true;
            break;
        }
    }

    return (
        <section className="vh-100">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6 mx-auto">
                    <h2 className="mb-5 text-center">Create new poll</h2>

                    <form className="create-form mx-auto">
                        <div className="mb-1">Title</div>
                        <div className="form-outline mb-2">
                            <input 
                                type="text"
                                id="pollTitle"
                                value={pollTitle}
                                onChange={(e) => setPollTitle(e.target.value)}
                                className="form-control"
                                placeholder="Enter title..."
                            />
                        </div>

                        {renderOptionInputs()}

                        <div className="pt-1 mt-3 text-center">
                            <button 
                                className="btn btn-success btn-md btn-block" 
                                type="button" 
                                onClick={() => addOption()}>
                                <i className="fa-solid fa-plus"></i> Add option
                            </button>
                        </div>

                        <div className="pt-1 mt-5 text-center">
                            <button 
                                className="btn btn-success btn-lg btn-block button-create-poll" 
                                type="button" 
                                disabled={emptyFields}
                                onClick={() => onSubmit()}>
                                Create poll
                            </button>
                        </div>
                    </form>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default CreatePoll;
