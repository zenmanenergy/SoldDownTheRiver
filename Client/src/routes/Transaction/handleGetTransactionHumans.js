// src/routes/Transactions/handleGet.js
import { baseURL } from '../Settings';
export async function handleGetTransactionHumans(SessionId,TransactionId, callback) {
  
  const url=`${baseURL}/Transaction/GetTransactionHumans?TransactionId=${TransactionId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  callback(data);
}
