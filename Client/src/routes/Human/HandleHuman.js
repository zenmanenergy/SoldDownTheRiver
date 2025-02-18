import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

/**
 * Fetch a single human's details by ID.
 * @param {string} sessionId - The session ID for authentication.
 * @param {string} HumanId - The ID of the human to fetch.
 * @returns {Promise<Object|null>} - Returns the human data or null if an error occurs.
 */
export async function handleGetHumanById(sessionId, HumanId) {
	const Data = { sessionId, HumanId };
	const url = baseURL + '/Human/GetHuman?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || typeof data !== 'object') {
		console.error("Invalid data received from API:", data);
		return null;
	}

	return data;
}

