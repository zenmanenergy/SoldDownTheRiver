// src/routes/Locations/handleDelete.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDelete(SessionId,LocationId) {
	const Data = {
		SessionId:SessionId,
		LocationId:LocationId
	};
	const url = baseURL + '/Location/DeleteLocation?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Locations';
}
