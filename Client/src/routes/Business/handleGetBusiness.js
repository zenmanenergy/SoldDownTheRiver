import { baseURL } from '../Settings';

export async function handleGetBusiness(SessionId, BusinessId, callback) {
    const url = `${baseURL}/Business/GetBusiness?BusinessId=${BusinessId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    callback(data);
}
  