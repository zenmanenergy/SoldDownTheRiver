// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleGetHumans(SessionId,  setData) {
    const url = `${baseURL}/Business/GetHumans?SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setData(data);
}
  