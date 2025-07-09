
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';
export async function handleGetTransactionHumans(SessionId,TransactionId, callback) {

	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId
	};
	const url = baseURL + '/Transaction/GetTransactionHumans?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
