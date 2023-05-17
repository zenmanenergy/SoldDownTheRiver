import { baseURL } from '../Settings';

export async function handleGet(SessionId, VoyageId, callback) {
  const url = `${baseURL}/Voyage/GetVoyage?VoyageId=${VoyageId}&SessionId=${SessionId}`;
  console.log(url);
  const response = await fetch(url);
  const data = await response.json();

  callback(data);
}
