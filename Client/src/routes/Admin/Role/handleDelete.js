// src/routes/Roles/handleDelete.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleDelete(SessionId,RoleId) {

	const Data = {
		SessionId:SessionId,
		RoleId:RoleId
	};
	const url = baseURL + '/Role/DeleteRole?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Admin/Roles';
}
