// src/routes/Users/handleGet.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleGetUser(SessionId,UserId, callback) {

	const Data = {
		SessionId:SessionId,
		UserId:UserId
	};
	const url = baseURL + '/User/GetUser?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
