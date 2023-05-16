
import { baseURL } from '../Settings';
export async function handleDeleteVoyageHuman(SessionId,VoyageId,HumanId) {
  try {
    const url=`${baseURL}/Voyage/DeleteVoyageHuman?VoyageId=${VoyageId}&HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Voyage with ID ${VoyageId} has been deleted.`);
    
    window.location.href = `/Voyage?VoyageId=${VoyageId}`;
  } catch (error) {
    console.error('There was a problem deleting the Voyage:', error);
  }
}
