// src/routes/Businesses/handleGet.js
const baseURL = 'http://192.168.1.182';
// src/routes/Business/handleGet.js
export async function handleGet(SessionId, BusinessId, setName) {
    const response = await fetch(`${baseURL}/Business/GetBusiness?BusinessId=${BusinessId}&SessionId=${SessionId}`);
    const data = await response.json();
  
    setName(data.BusinessName);
}
  