import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetHumans(SessionId,RoleId, Query,callback) {

	const Data = {
		SessionId:SessionId,
		Query:Query,
		RoleId:RoleId
	}
	const url = baseURL + '/Role/GetHumans?'
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
