import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetShips(SessionId,HumanId, callback) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Human/ShipOwner/GetShips?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}