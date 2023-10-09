// src/routes/Users/handleDelete.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDelete(SessionId,UserId) {

	const Data = {
		SessionId:SessionId,
		UserId:UserId
	};
	const url = baseURL + '/User/DeleteUser?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = "/Users";
}
