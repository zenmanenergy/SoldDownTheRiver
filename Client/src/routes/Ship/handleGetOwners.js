import { baseURL } from '../Settings';

export async function handleGetOwners(SessionId, ShipId, callback) {
  const url=`${baseURL}/Ship/GetOwners?SessionId=${SessionId}&ShipId=${ShipId}`
  console.log(url)
  const response = await fetch(url);
  const Humans = await response.json();
  callback(Humans);
}
