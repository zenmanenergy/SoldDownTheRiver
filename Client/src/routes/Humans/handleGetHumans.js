import { baseURL } from '../Settings';

export async function handleGetHumans(SessionId, callback) {
  const url=`${baseURL}/Humans/GetHumans?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const Humans = await response.json();
  callback(Humans);
}
