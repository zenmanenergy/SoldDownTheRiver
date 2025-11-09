import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSearchLocations(callback) {
	const Data = {};
	const url = baseURL + '/Locations/GetSearchLocations?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	// Format the data, replace null values with empty strings
	const formattedData = data.map(location => ({
		...location,
		LocationId: location.LocationId || '',
		Name: location.Name || '',
		LocationType: location.LocationType || '',
		Address: location.Address || '',
		City: location.City || '',
		County: location.County || '',
		StateAbbr: location.StateAbbr || '',
		Description: location.Description || ''
	}));

	callback(formattedData);
}
