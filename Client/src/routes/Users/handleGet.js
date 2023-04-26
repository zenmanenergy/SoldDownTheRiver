import { baseURL } from '../Settings';

async function handleGet(SessionId) {
  const url=`${baseURL}/Users/GetUsers?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const users = await response.json();
  return users;
}

export default handleGet;
