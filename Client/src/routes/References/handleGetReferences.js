import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetReferences(SessionId, callback) {
	const Data = { SessionId };
	const url = baseURL + '/References/GetReferences?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	// Format the references, replace null values with empty strings
	const formattedData = data.map(reference => ({
		...reference,
		ReferenceId: reference.ReferenceId || '',
		URL: reference.URL || '',
		Notes: reference.Notes || '',
		dateUpdated: reference.dateUpdated || ''
	}));

	callback(formattedData);
}
