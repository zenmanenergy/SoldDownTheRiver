import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

/**
 * Fetch a single transaction.
 * @param {string} SessionId - The session ID for authentication.
 * @param {string} TransactionId - The ID of the transaction to retrieve.
 * @returns {Promise<Object|null>} - The transaction data or null if an error occurs.
 */
export async function handleGetTransaction(TransactionId) {
	const Data = { TransactionId };
	const url = baseURL + '/Transaction/GetTransaction?';
	const FormValid = true;

	try {
		let data = await SuperFetch(url, Data, FormValid);

		if (!data || data.error) {
			console.error("Error fetching transaction:", data?.error || "Unknown error");
			return null;
		}
		console.log(data)
		return data;
	} catch (error) {
		console.error("handleGetTransaction error:", error);
		return null;
	}
}
