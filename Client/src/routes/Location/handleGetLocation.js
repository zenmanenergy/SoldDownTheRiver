
import { baseURL } from '../Settings';
export async function handleGetLocation(SessionId,LocationId, callback) {
    const url=`${baseURL}/Location/GetLocation?LocationId=${LocationId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    callback(data);
}
