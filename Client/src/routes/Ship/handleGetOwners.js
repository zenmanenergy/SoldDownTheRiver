import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetOwners(SessionId, ShipId, callback) {

	const Data = {
		SessionId:SessionId,
		ShipId:ShipId
	};
	const url = baseURL + '/Ship/GetOwners?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
