import { baseURL } from '../Settings';

export async function handleGetVoyageHumans(SessionId, VoyageId, callback) {
  const url=`${baseURL}/Voyage/GetVoyageHumans?SessionId=${SessionId}&VoyageId=${VoyageId}`
  console.log(url)
  const response = await fetch(url);
  const Humans = await response.json();
  callback(Humans);
}
