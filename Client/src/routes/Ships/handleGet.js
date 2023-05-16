import { baseURL } from '../Settings';

export async function handleGet(SessionId, callback) {
  const url = `${baseURL}/Ships/GetShips?SessionId=${SessionId}`;
  console.log(url);
  const response = await fetch(url);
  const ships = await response.json();
  callback(ships);
}

