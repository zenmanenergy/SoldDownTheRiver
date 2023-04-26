// src/routes/Locations/handleDelete.js
import { baseURL } from '../Settings';
export async function handleDelete(SessionId,LocationId) {
  try {
    const url=`${baseURL}/Location/DeleteLocation?LocationId=${LocationId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Location with ID ${LocationId} has been deleted.`);
    window.location.href = '/Locations';
  } catch (error) {
    console.error('There was a problem deleting the location:', error);
  }
}
