// src/routes/Humans/handleGetAKA.js
import { baseURL } from '../Settings';

export async function handleGetRoles(SessionId,setRoles) {
  const url=`${baseURL}/Human/GetRoles?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setRoles(data);
}