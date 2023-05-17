import { baseURL } from '../Settings';

export async function handleGet(SessionId, callback) {
  const url=`${baseURL}/Locations/GetLocations?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const locations = await response.json();
  callback(locations);
}

