import { baseURL } from '../Settings';

async function handleGet(SessionId) {
  const url = `${baseURL}/Voyages/GetVoyages?SessionId=${SessionId}`; // Update the API endpoint for voyages
  console.log(url);
  const response = await fetch(url);
  const voyages = await response.json(); // Update the variable name to `voyages`
  return voyages;
}

export default handleGet;
