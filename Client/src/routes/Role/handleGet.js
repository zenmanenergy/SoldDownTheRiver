// src/routes/Roles/handleGet.js
const baseURL = 'http://192.168.1.182';

export async function handleGet(SessionId,RoleId, setRole) {
    const response = await fetch(`${baseURL}/Role/GetRole?RoleId=${RoleId}&SessionId=${SessionId}`);
    const data = await response.json();
  
    setRole(data.RoleId,data.Role);
}
