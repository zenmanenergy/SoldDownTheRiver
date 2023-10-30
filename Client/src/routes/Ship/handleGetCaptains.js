import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetCaptains(SessionId, Query,callback) {

	const Data = {
		SessionId:SessionId,
		Query:Query,
	}
	const url = baseURL + '/Ship/GetCaptains?'
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
