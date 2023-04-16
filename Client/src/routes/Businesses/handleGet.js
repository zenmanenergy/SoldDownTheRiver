const baseURL = 'http://192.168.1.182';

async function handleGet() {
  const response = await fetch(`${baseURL}/GetBusinesses`);
  const businesses = await response.json();
  return businesses;
}

export default handleGet;