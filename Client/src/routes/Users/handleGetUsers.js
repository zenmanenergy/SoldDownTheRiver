import { baseURL } from '../Settings';

export async function handleGetUsers(SessionId, callback) {
  const url=`${baseURL}/Users/GetUsers?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const Users = await response.json();
  callback(Users);
}

