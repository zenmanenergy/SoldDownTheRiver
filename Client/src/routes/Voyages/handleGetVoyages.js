import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetVoyages(SessionId, callback) {

	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Voyages/GetVoyages?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)
	console.log(data)
	callback(data);
}
