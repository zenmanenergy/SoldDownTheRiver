const baseURL = 'http://192.168.1.182';

async function handleGet() {
  const response = await fetch(`${baseURL}/GetLocations`);
  const locations = await response.json();
  return locations;
}

export default handleGet;
