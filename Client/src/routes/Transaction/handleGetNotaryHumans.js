// src/routes/Transactions/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGetNotaryHumans(SessionId,TransactionId, setTransactionData) {
  const url=`${baseURL}/Transaction/GetNotaryHumans?TransactionId=${TransactionId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setTransactionData(data);
}
