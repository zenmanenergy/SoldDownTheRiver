import { baseURL } from '../Settings';

export async function handleGetLocations(SessionId, callback) {

	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Voyage/GetLocations?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}