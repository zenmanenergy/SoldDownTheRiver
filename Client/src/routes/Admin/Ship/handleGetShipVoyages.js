// src/routes/Ships/handleGet.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetShipVoyages(SessionId, ShipId, callback) {

	const Data = {
		SessionId:SessionId,
		ShipId:ShipId
	};
	const url = baseURL + '/Ship/GetShipVoyages?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
