// src/routes/Locations/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Locations/handleGet.js
export async function handleGet(SessionId,LocationId, callback) {
    const url=`${baseURL}/Location/GetLocation?LocationId=${LocationId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    callback(data);
}
