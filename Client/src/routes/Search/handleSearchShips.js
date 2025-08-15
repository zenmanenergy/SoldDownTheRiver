import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSearchShips(callback) {
	const Data = {};
	const url = baseURL + '/Ships/GetShips?'; 
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	// Format the data, replace null values with empty strings
	const formattedData = data.map(ship => ({
		...ship, // Spread original ship data
		ShipName: ship.ShipName || '',
		ShipType: ship.ShipType || '',
		Flag: ship.Flag || '',
		Captains: ship.Captains || '', // Add this line
		Owner: ship.Owner || '',
		Builder: ship.Builder || '',
		BuildYear: ship.BuildYear || '',
		Tonnage: ship.Tonnage || '',
		Description: ship.Description || ''
	}));

	callback(formattedData);
}

