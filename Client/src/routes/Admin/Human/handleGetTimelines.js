import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

/**
 * Fetch a human's timelines by ID.
 * @param {string} SessionId - The session ID for authentication.
 * @param {string} HumanId - The ID of the human to fetch timelines for.
 * @returns {Promise<Object|null>} - Returns the timelines data or null if an error occurs.
 */
export async function handleGetTimelines(SessionId, HumanId) {
	const Data = { SessionId, HumanId };
	const url = baseURL + '/Human/GetTimelines?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || typeof data !== 'object') {
		console.error("Invalid data received from API:", data);
		return null;
	}

	return data;
}
