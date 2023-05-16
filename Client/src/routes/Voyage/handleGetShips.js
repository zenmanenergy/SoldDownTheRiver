import { baseURL } from '../Settings';

export async function handleGetShips(SessionId, callback) {
  const url = `${baseURL}/Voyage/GetShips?SessionId=${SessionId}`;
  console.log(url);
  const response = await fetch(url);
  const ships = await response.json();
  callback(ships);
}
