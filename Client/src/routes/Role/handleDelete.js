// src/routes/Roles/handleDelete.js
const baseURL = 'http://192.168.1.182';

export async function handleDelete(RoleId) {
  console.log(`${baseURL}/Role/DeleteRole?RoleId=${RoleId}`)
  try {
    const response = await fetch(`${baseURL}/Role/DeleteRole?RoleId=${RoleId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Role with name "${RoleId}" has been deleted.`);
    window.location.href = '/Roles';
  } catch (error) {
    console.error('There was a problem deleting the role:', error);
  }
}
