import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

/**
 * Fetch the combined timeline for a human by ID.
 * @param {string} HumanId - The ID of the human to fetch the combined timeline for.
 * @returns {Promise<Object|null>} - Returns the combined timeline data or null if an error occurs.
 */
export async function handleGetCombinedTimeline(HumanId) {
	const Data = { HumanId };
	const url = baseURL + '/Human/GetCombinedTimeline?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || typeof data !== 'object') {
		console.error("Invalid data received from API:", data);
		return null;
	}

	return data;
}
