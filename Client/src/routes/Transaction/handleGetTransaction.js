
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleGetTransaction(SessionId,TransactionId, callback) {

	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId
	};
	const url = baseURL + '/Transaction/GetTransaction?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
