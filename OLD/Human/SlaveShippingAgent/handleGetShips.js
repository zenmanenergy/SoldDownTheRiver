import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetShips(SessionId,HumanId, callback) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Human/ShipAgent/GetShips?'; 
	console.log(url)
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
