import { baseURL } from '../../../Settings';
import { SuperFetch } from '../../../SuperFetch';

export async function handleGetHumans(SessionId, callback) {
	const Data = { SessionId };
	const url = baseURL + '/Humans/GetHumans?'; 
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	// Format the roles properly
	const formattedData = data.map(human => ({
		...human, // Spread original human data
		Roles: human.Roles ? human.Roles.split(', ') : [] // Convert Roles string to an array, or set to an empty array if null
	}));

	callback(formattedData);
}
