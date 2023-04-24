// src/routes/Roles/handleGet.js
const baseURL = 'http://192.168.1.182';

export async function handleGet(SessionId,RoleId, setRole) {
    const url="${baseURL}/Role/GetRole?RoleId=${RoleId}&SessionId=${SessionId}"
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setRole(data.RoleId,data.Role);
}
