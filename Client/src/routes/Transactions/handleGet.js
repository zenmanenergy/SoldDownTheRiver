const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId,) {
  const url=`${baseURL}/Transactions/GetTransactions?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const transactions = await response.json();
  return transactions;
}

export default handleGet;
