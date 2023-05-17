// src/routes/Roles/handleGet.js
import { baseURL } from '../Settings';

export async function handleGetRole(SessionId,RoleId,callback) {
    const url=`${baseURL}/Role/GetRole?RoleId=${RoleId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    callback(data);
}
