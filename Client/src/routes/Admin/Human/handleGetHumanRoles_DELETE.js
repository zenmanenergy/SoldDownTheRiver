import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetHumanRoles(SessionId,HumanId, callback) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Human/GetHumanRoles?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
