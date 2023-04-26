// src/routes/Businesses/handleDelete.js
import { baseURL } from '../Settings';
export async function handleDelete(SessionId, BusinessId) {
  try {
    const url=`${baseURL}/Business/DeleteBusiness?BusinessId=${BusinessId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Business with ID ${BusinessId} has been deleted.`);
    window.location.href = '/Businesses';
  } catch (error) {
    console.error('There was a problem deleting the business:', error);
  }
}
