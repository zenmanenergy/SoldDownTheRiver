// src/routes/Ships/handleDelete.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleDelete(SessionId, ShipId) {

	const Data = {
		SessionId:SessionId,
		ShipId:ShipId
	};
	const url = baseURL + '/Ship/DeleteShip?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = "/Ships";
}
