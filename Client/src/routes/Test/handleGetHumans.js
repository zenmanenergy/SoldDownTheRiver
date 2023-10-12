import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetHumans(SessionId, Query, callback) {


	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + "/Humans/GetHumans?Query="+Query+"&"; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);

}
