// src/routes/Locations/handleDelete.js
const baseURL = 'http://192.168.1.182';
export async function handleDelete(LocationId) {
  try {
    const response = await fetch(`${baseURL}/DeleteLocation?LocationId=${LocationId}`);
    

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Location with ID ${LocationId} has been deleted.`);
    window.location.href = '/Locations';
  } catch (error) {
    console.error('There was a problem deleting the location:', error);
  }
}
