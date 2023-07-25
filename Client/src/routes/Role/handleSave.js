import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

// src/routes/Roles/handleSave.js
export async function handleSave(SessionId,Role, formValid) {
	

	const Data = {
		SessionId:SessionId,
		Role:Role
	};
	const url = baseURL + '/Role/SaveRole?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Roles';
}
