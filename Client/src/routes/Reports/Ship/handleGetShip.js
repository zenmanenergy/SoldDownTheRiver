// src/routes/Ships/handleGet.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetShip( ShipId, callback) {

	const Data = {
		ShipId:ShipId
	};
	const url = baseURL + '/Ship/GetShip?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
