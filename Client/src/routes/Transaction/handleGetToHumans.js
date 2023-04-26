// src/routes/Transactions/handleGet.js
import { baseURL } from '../Settings';
export async function handleGetToHumans(SessionId,TransactionId, setTransactionData) {
  const url=`${baseURL}/Transaction/GetToHumans?TransactionId=${TransactionId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setTransactionData(data);
}
