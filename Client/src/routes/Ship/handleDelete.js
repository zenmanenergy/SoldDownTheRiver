// src/routes/Ships/handleDelete.js
import { baseURL } from '../Settings';

export async function handleDelete(SessionId, ShipId) {
  try {
    const url = `${baseURL}/Ship/DeleteShip?ShipId=${ShipId}&SessionId=${SessionId}`;
    console.log(url);
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Ship with ID ${ShipId} has been deleted.`);
    window.location.href = "/Ships";
  } catch (error) {
    console.error("There was a problem deleting the ship:", error);
  }
}
