// src/routes/Transactions/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGetFromHumans(TransactionId, setTransactionData) {
  console.log(`${baseURL}/Transaction/GetFromHumans?TransactionId=${TransactionId}`)
  const response = await fetch(`${baseURL}/Transaction/GetFromHumans?TransactionId=${TransactionId}`);
  const data = await response.json();

  setTransactionData(data);
}
