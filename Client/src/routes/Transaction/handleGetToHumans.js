// src/routes/Transactions/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGetToHumans(SessionId,TransactionId, setTransactionData) {
  const url=`${baseURL}/Transaction/GetToHumans?TransactionId=${TransactionId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setTransactionData(data);
}
