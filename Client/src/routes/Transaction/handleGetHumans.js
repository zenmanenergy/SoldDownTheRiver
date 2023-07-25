// src/routes/Transactions/handleGet.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleGetHumans(SessionId,TransactionId, callback) {
  

	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId
	};
	const url = baseURL + '/Transaction/GetHumans?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
