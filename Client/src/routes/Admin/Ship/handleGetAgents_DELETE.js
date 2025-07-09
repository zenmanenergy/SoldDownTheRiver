import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetAgents(SessionId, Query,callback) {

	const Data = {
		SessionId:SessionId,
		Query:Query,
	}
	const url = baseURL + '/Ship/GetAgents?'
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
