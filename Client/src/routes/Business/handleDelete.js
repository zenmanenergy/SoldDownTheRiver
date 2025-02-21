// src/routes/Businesses/handleDelete.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDelete(SessionId, BusinessId) {

	const Data = {
		SessionId:SessionId,
		BusinessId:BusinessId
	};
	const url = baseURL + '/Business/DeleteBusiness?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Businesses';
}
