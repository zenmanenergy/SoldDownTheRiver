// src/routes/Locations/handleGet.js
const baseURL = 'http://192.168.1.182';
// src/routes/Locations/handleGet.js
export async function handleGet(SessionId,LocationId, setLocation) {
    const response = await fetch(`${baseURL}/Location/GetLocation?LocationId=${LocationId}&SessionId=${SessionId}`);
    const data = await response.json();
  
    setLocation(data.City, data.State, data.Country, data.Latitude, data.Longitude);
}
