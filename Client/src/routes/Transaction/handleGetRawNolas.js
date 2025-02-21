// src/routes/Transactions/handleGetRawNola.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetRawNolas(SessionId, NOLAIds, callback) {
	// Ensure NOLAIds is an array
	const Data = {
		SessionId: SessionId,
		NOLAId: NOLAIds.join(",") // Convert array to comma-separated string
	};
	const url = baseURL + '/RawNOLA/GetRawNOLAs?'; 
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	callback(data);
}
