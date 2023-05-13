import { baseURL } from '../Settings';

async function handleGet(SessionId) {
  const url = `${baseURL}/Ships/GetShips?SessionId=${SessionId}`;
  console.log(url);
  const response = await fetch(url);
  const ships = await response.json();
  return ships;
}

export default handleGet;
