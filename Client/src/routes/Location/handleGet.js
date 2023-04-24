// src/routes/Locations/handleGet.js
const baseURL = 'http://192.168.1.182';
// src/routes/Locations/handleGet.js
export async function handleGet(SessionId,LocationId, setLocation) {
    const url=`${baseURL}/Location/GetLocation?LocationId=${LocationId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setLocation(data.City, data.State, data.Country, data.Latitude, data.Longitude);
}
