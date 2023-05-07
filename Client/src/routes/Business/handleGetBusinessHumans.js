// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleGetBusinessHumans(SessionId, BusinessId, setData) {
    const url = `${baseURL}/Business/GetBusinessHumans?BusinessId=${BusinessId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setData(data);
}
  