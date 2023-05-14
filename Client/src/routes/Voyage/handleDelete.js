import { baseURL } from '../Settings';

export async function handleDelete(SessionId, VoyageId) {
  try {
    const url = `${baseURL}/Voyage/DeleteVoyage?VoyageId=${VoyageId}&SessionId=${SessionId}`;
    console.log(url);
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Voyage with ID ${VoyageId} has been deleted.`);
    window.location.href = '/Voyages';
  } catch (error) {
    console.error('There was a problem deleting the voyage:', error);
  }
}
