import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

// src/routes/Roles/handleSave.js
export async function handleSave(SessionId,Role, FormValid) {
	

	const Data = {
		SessionId:SessionId,
		RoleId:Role.RoleId,
		Role:Role.Role,
	};
	const url = baseURL + '/Role/SaveRole?'; 
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Roles';
}
