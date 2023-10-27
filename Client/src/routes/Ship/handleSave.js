import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

// src/routes/Ships/handleSave.js
export async function handleSave(SessionId, ShipData, FormValid) {
	
	ShipData.SessionId = SessionId;
	// if (ShipData.BuildDate instanceof Date) {
	// 	ShipData.BuildDate = ShipData.BuildDate.toISOString();
	// } else {
	// 	ShipData.BuildDate = "";
	// }
	console.log("SHIPDATA",ShipData)
	const url = baseURL + '/Ship/SaveShip?'; 
	let data = await SuperFetch(url, ShipData, FormValid)

	window.location.href = '/Ships';
}
