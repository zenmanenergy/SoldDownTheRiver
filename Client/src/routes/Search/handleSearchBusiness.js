// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleSearch(SessionId, BusinessName, callbackfunction) {
    const url = `${baseURL}/Search/SearchBusiness?BusinessName=${BusinessName}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    callbackfunction(data.BusinessName, data.LastModified);
}
  