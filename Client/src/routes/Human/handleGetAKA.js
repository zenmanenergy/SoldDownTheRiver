import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetAKA(SessionId,HumanId, callback) {
	

	const Data = {
		HumanId:HumanId,
		SessionId:SessionId
	};
	const url = baseURL + '/Human/GetAkaNames?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}