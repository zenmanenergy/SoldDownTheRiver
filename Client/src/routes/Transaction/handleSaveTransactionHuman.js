// src/routes/Transactions/handleGet.js
import { baseURL } from '../Settings';
export async function handleSaveTransactionHuman(SessionId,TransactionId, HumanId, callback) {
  
  const url=`${baseURL}/Transaction/SaveTransactionHuman?TransactionId=${TransactionId}&HumanId=${HumanId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();
  callback(data[0]);
}
