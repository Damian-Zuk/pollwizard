import PollForm from "../components/PollForm";
import { PollFormProps } from "../components/PollForm";
import { useState, useEffect } from 'react';
import { useAuthHeader } from 'react-auth-kit'
import { useIsAuthenticated } from 'react-auth-kit';
import axios from "axios";

function Home() {
  const [data, setData] = useState<PollFormProps[]>([]);

  const isAuth = useIsAuthenticated()
  const authHeader = useAuthHeader()

  const header = isAuth() ? {Authorization: authHeader()} : {}
  const endpoint = isAuth() ? "all-auth" : "all"

  useEffect(() => {
    axios
      .get(`http://localhost:8000/polls/${endpoint}`, {headers: header})
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div className="vh-100 container">
      {data.map((entry: PollFormProps) => (
        <PollForm {...entry}  _title_is_link={true} key={entry.id}/>
      ))}
      {data.length == 0 && <h2 className="text-center">No poll has been created yet :(</h2>}
    </div>
  );
}

export default Home;
