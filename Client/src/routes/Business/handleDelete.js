// src/routes/Businesses/handleDelete.js
const baseURL = 'http://192.168.1.182';
export async function handleDelete(BusinessId) {
  try {
    const response = await fetch(`${baseURL}/Business/DeleteBusiness?BusinessId=${BusinessId}`);
    

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Business with ID ${BusinessId} has been deleted.`);
    window.location.href = '/Businesses';
  } catch (error) {
    console.error('There was a problem deleting the business:', error);
  }
}
