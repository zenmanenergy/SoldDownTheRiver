// src/routes/Transactions/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGet(SessionId,TransactionId, setTransactionData) {
  console.log(`${baseURL}/Transaction/GetTransaction?TransactionId=${TransactionId}&SessionId=${SessionId}`)
  const response = await fetch(`${baseURL}/Transaction/GetTransaction?TransactionId=${TransactionId}&SessionId=${SessionId}`);
  const data = await response.json();

  setTransactionData(data);
}
