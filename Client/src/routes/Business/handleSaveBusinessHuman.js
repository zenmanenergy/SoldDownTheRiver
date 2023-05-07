// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleSaveBusinessHuman(SessionId, BusinessId, HumanId) {
    const url = `${baseURL}/Business/SaveBusinessHuman?BusinessId=${BusinessId}&HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
}
  