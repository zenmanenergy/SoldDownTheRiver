const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  const response = await fetch(`${baseURL}/Locations/GetLocations?SessionId=${SessionId}`);
  const locations = await response.json();
  return locations;
}

export default handleGet;
