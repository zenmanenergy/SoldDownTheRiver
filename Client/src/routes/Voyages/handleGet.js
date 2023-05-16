import { baseURL } from '../Settings';

export async function handleGet(SessionId, callback) {
  const url = `${baseURL}/Voyages/GetVoyages?SessionId=${SessionId}`; // Update the API endpoint for Voyages
  console.log(url);
  const response = await fetch(url);
  const Voyages = await response.json(); // Update the variable name to `Voyages`
  callback(Voyages);
}
