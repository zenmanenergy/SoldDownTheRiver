import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetReference(SessionId, ReferenceId) {
	const Data = { SessionId, ReferenceId };
	const url = baseURL + '/References/GetReference?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	if (!data || typeof data !== 'object') {
		console.error("Invalid data received from API:", data);
		return null;
	}

	return {
		ReferenceId: data.ReferenceId || '',
		URL: data.URL || '',
		Notes: data.Notes || '',
		dateUpdated: data.dateUpdated || ''
	};
}
