// src/routes/Transactions/handleDelete.js
const baseURL = 'http://192.168.1.182';
export async function handleDelete(TransactionId) {
  try {
    const response = await fetch(`${baseURL}/Transaction/DeleteTransaction?TransactionId=${TransactionId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Transaction with ID ${TransactionId} has been deleted.`);
    window.location.href = '/Transactions';
  } catch (error) {
    console.error('There was a problem deleting the transaction:', error);
  }
}
