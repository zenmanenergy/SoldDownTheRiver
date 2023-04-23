// src/routes/Transactions/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGetFromHumans(SessionId,TransactionId, setTransactionData) {
  console.log(`${baseURL}/Transaction/GetFromHumans?TransactionId=${TransactionId}&SessionId=${SessionId}`)
  const response = await fetch(`${baseURL}/Transaction/GetFromHumans?TransactionId=${TransactionId}&SessionId=${SessionId}`);
  const data = await response.json();

  setTransactionData(data);
}
