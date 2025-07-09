// src/routes/Roles/handleDelete.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleDeleteHumanRole(SessionId,RoleId,HumanId) {

	const Data = {
		SessionId:SessionId,
		RoleId:RoleId,
		HumanId:HumanId
	};
	const url = baseURL + '/Role/DeleteHumanRole?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Admin/Role?RoleId='+RoleId;
}
