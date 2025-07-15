
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';
export async function handleGetLocationTimelines(SessionId,LocationId, callback) {
	

	
	const Data = {
		SessionId:SessionId,
		LocationId:LocationId
	};
	const url = baseURL + '/Location/GetTimelines?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
