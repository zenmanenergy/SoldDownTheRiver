// src/routes/Roles/handleGet.js
const baseURL = 'http://192.168.1.182';

export async function handleGet(RoleId, setName) {
    const response = await fetch(`${baseURL}/GetRole?RoleId=${RoleId}`);
    const data = await response.json();
  
    setName(data.RoleId,data.Role);
}
