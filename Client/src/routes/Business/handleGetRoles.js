	
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleGetRoles(SessionId,  callback) {
	

	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/Business/GetRoles?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
  