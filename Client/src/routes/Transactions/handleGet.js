const baseURL = 'http://192.168.1.182';

async function handleGet() {
  const response = await fetch(`${baseURL}/Transactions/GetTransactions`);
  const transactions = await response.json();
  return transactions;
}

export default handleGet;
