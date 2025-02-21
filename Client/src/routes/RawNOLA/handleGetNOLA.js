import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetNOLA(SessionId, NOLA_ID, callback) {
	if (!NOLA_ID) {
		console.error("Error: NOLA_ID is missing.");
		return;
	}

	const Data = {
		SessionId: SessionId,
		NOLAId: NOLA_ID  // Use "NOLAId" to match the Flask route parameter
	};
	const url = baseURL + '/RawNOLA/GetRawNOLAs?';

	console.log("Fetching NOLA record:", url, Data);

	const FormValid = true;
	let data = await SuperFetch(url, Data, FormValid);

	if (!data || data.length === 0) {
		console.error("Error: API returned empty or undefined data.", data);
		return;
	}

	console.log("Received NOLA Data:", data[0]);
	callback(data[0]);  // Extract the first record from the list
}
