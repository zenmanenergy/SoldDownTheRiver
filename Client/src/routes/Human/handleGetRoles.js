// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetRoles(SessionId,setRoles) {
  const url="${baseURL}/Human/GetRoles?SessionId=${SessionId}"
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setRoles(data);
}