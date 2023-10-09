import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetPossibleFamilies(SessionId,HumanId,callback) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Human/GetPossibleFamilies?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}


