// src/routes/Transactions/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGet(TransactionId, setTransactionData) {
  console.log(`${baseURL}/Transaction/GetTransaction?TransactionId=${TransactionId}`)
  const response = await fetch(`${baseURL}/Transaction/GetTransaction?TransactionId=${TransactionId}`);
  const data = await response.json();

  setTransactionData(data);
}
