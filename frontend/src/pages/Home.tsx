import PollForm from "../components/PollForm";
import { PollFormProps } from "../components/PollForm";
import { useState, useEffect } from 'react';
import axios from "axios";

function Home() {
  const [data, setData] = useState<PollFormProps[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/polls")
    .then((response) => {
      setData(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
  }, []);
  
  return (
    <div className="container">
      {data.map((entry: PollFormProps) => (
        <PollForm {...entry}/>
      ))}
    </div>
  );
}

export default Home;
