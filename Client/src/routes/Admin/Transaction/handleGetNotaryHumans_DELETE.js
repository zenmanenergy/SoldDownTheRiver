
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';
export async function handleGetNotaryHumans(SessionId,TransactionId, callback) {

	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId
	};
	const url = baseURL + '/Transaction/GetNotaryHumans?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
