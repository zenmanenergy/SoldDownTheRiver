// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetRoles(SessionId,setRoles) {
  console.log(`${baseURL}/Human/GetRoles?SessionId=${SessionId}`)
  const response = await fetch(`${baseURL}/Human/GetRoles?SessionId=${SessionId}`);
  const data = await response.json();

  setRoles(data);
}