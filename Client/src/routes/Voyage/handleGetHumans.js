import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetHumans(SessionId, VoyageId, callback) {

	const Data = {
		SessionId:SessionId,
		VoyageId:VoyageId
	};
	const url = baseURL + '/Voyage/GetHumans?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
