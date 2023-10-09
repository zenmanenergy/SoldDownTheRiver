
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleGetLocation(SessionId,LocationId, callback) {
	

	
	const Data = {
		SessionId:SessionId,
		LocationId:LocationId
	};
	const url = baseURL + '/Location/GetLocation?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
