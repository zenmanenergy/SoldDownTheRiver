// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleSaveBusinessHuman(SessionId, BusinessId, HumanId, RoleId) {
    const url = `${baseURL}/Business/SaveBusinessHuman?BusinessId=${BusinessId}&HumanId=${HumanId}&RoleId=${RoleId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
    window.location.href = `/Business?BusinessId=${BusinessId}`;
  
}
  