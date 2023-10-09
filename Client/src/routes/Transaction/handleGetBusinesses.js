import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetBusinesses(SessionId,callback) {
	

	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Transaction/GetBusinesses?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);

}