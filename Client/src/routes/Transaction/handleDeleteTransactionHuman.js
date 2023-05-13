
import { baseURL } from '../Settings';
export async function handleDeleteTransactionHuman(SessionId,TransactionId,HumanId) {
  try {
    const url=`${baseURL}/Transaction/DeleteTransactionHuman?TransactionId=${TransactionId}&HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Transaction with ID ${TransactionId} has been deleted.`);
    
    window.location.href = `/Transaction?TransactionId=${TransactionId}`;
  } catch (error) {
    console.error('There was a problem deleting the transaction:', error);
  }
}
