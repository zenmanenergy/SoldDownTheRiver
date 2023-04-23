const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId,) {
  const response = await fetch(`${baseURL}/Transactions/GetTransactions?SessionId=${SessionId}`);
  const transactions = await response.json();
  return transactions;
}

export default handleGet;
