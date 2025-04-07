import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSaveTransaction(SessionId, transactionId, transactionData) {
	const Data = { SessionId, transactionId, ...transactionData };
	const url = baseURL + '/Transaction/SaveTransaction?';  // ✅ Matches your API structure
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);

	// Ensure the request was successful
	if (!response || !response.success) {  // ✅ Consistent success check
		console.error("Failed to save transaction:", response);
		return false;
	}

	return response;
}
