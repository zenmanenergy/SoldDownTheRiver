// src/routes/Roles/handleDelete.js
import { baseURL } from '../Settings';

export async function handleDelete(SessionId,RoleId) {
  try {
    const url=`${baseURL}/Role/DeleteRole?RoleId=${RoleId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Role with name "${RoleId}" has been deleted.`);
    window.location.href = '/Roles';
  } catch (error) {
    console.error('There was a problem deleting the role:', error);
  }
}
