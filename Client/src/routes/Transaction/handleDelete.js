// src/routes/Transactions/handleDelete.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDelete(SessionId,TransactionId) {

	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId
	};
	const url = baseURL + '/Transaction/DeleteTransaction?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Transactions';
}
