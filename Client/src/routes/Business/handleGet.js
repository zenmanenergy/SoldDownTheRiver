// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleGet(SessionId, BusinessId, setName) {
    const url = `${baseURL}/Business/GetBusiness?BusinessId=${BusinessId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setName(data.BusinessName, data.LastModified);
}
  