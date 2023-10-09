import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetHuman(SessionId,HumanId, callback) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Human/GetHuman?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
