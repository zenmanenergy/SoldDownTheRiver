import { baseURL } from '../Settings';

async function handleGet(SessionId) {
  const url=`${baseURL}/Humans/GetHumans?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const Humans = await response.json();
  return Humans;
}

export default handleGet;