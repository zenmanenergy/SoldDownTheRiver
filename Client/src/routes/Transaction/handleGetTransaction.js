
import { baseURL } from '../Settings';
export async function handleGetTransaction(SessionId,TransactionId, setTransactionData) {
  
  const url=`${baseURL}/Transaction/GetTransaction?TransactionId=${TransactionId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();
  setTransactionData(data[0]);
}
