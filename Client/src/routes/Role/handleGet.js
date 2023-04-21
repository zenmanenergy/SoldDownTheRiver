// src/routes/Roles/handleGet.js
const baseURL = 'http://192.168.1.182';

export async function handleGet(RoleId, setRole) {
    const response = await fetch(`${baseURL}/GetRole?RoleId=${RoleId}`);
    const data = await response.json();
  
    setRole(data.RoleId,data.Role);
}
