// src/routes/Businesses/handleGet.js
const baseURL = 'http://192.168.1.182';
// src/routes/Businesses/handleGet.js
export async function handleGet(BusinessId, setName) {
    const response = await fetch(`${baseURL}/GetBusiness?BusinessId=${BusinessId}`);
    const data = await response.json();
  
    setName(data.BusinessName);
}
  