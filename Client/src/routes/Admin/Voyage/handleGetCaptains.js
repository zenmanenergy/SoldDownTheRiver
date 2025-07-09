import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetCaptains(SessionId, callback) {
	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Voyage/GetCaptains?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
