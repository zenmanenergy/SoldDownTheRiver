// src/routes/Roles/handleGet.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetRoleHumans(SessionId,RoleId,callback) {

	const Data = {
		SessionId:SessionId,
		RoleId:RoleId
	};
	const url = baseURL + '/Role/GetRoleHumans?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
