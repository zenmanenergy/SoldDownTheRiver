import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetLinkReferences(LinkId, TargetType, callback) {
	const Data = { LinkId, TargetType };
	const url = baseURL + '/References/GetLinkReferences?';
	const FormValid = true;
	let data = await SuperFetch(url, Data, FormValid);

	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	const formattedData = data.map(reference => ({
		...reference,
		ReferenceId: reference.ReferenceId || '',
		URL: reference.URL || '',
		Notes: reference.Notes || '',
		dateUpdated: reference.dateUpdated || ''
	}));

	callback(formattedData);
}
