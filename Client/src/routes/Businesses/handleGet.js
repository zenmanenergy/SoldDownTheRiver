const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  const response = await fetch(`${baseURL}/Businesses/GetBusinesses?SessionId=${SessionId}`);
  const businesses = await response.json();
  return businesses;
}

export default handleGet;