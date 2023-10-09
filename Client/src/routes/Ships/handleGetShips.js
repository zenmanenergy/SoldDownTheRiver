import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetShips(SessionId, callback) {

	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Ships/GetShips?SessionId?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}

