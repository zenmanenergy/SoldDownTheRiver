// src/routes/Transactions/handleGet.js
import { baseURL } from '../Settings';
export async function handleSaveTransactionHuman(SessionId,TransactionId, HumanId,Price,Notes, callback) {
  
  const url=`${baseURL}/Transaction/SaveTransactionHuman?TransactionId=${TransactionId}&HumanId=${HumanId}&Price=${Price}&Notes=${Notes}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();
  callback(data[0]);
  window.location.href = `/Transaction?TransactionId=${TransactionId}`;
}
