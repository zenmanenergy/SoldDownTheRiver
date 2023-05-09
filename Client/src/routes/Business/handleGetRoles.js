    
import { baseURL } from '../Settings';
export async function handleGetRoles(SessionId,  setData) {
    const url = `${baseURL}/Business/GetRoles?SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setData(data);
}
  