import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetTransactions(SessionId,callback) {
	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Transactions/GetTransactions?SessionId?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}

