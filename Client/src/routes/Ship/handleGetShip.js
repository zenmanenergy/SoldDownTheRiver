// src/routes/Ships/handleGet.js
import { baseURL } from '../Settings';

export async function handleGetShip(SessionId, ShipId, callback) {
  const url = `${baseURL}/Ship/GetShip?ShipId=${ShipId}&SessionId=${SessionId}`;
  console.log(url);
  const response = await fetch(url);
  const data = await response.json();

  callback(data);
}
