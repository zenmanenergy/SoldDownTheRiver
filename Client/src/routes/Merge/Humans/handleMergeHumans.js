import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleMergeHumans(SessionId, HumanId, MergeHumanId, callback) {
	const Data = { SessionId, HumanId, MergeHumanId };
	const url = baseURL + '/HumanMerge/Save?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !data.success) {
		console.error("Failed to merge humans:", data);
		callback(null);
		return;
	}

	callback(data);
}
