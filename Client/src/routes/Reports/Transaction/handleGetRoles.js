import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetRoles(callback) {
	

	const Data = {
	};
	const url = baseURL + '/Roles/GetRoles?SessionId?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
