import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

/**
 * Fetch a single human's details by ID.
 * @param {string} sessionId - The session ID for authentication.
 * @param {string} humanId - The ID of the human to fetch.
 * @returns {Promise<Object|null>} - Returns the human data or null if an error occurs.
 */
export async function handleGetHumanById(sessionId, humanId) {
	const Data = { sessionId, humanId };
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

/**
 * Save or update human data.
 * @param {string} sessionId - The session ID for authentication.
 * @param {string|null} humanId - The ID of the human being updated (null for new records).
 * @param {Object} humanData - The human data to save.
 * @returns {Promise<boolean>} - Returns true if successful, false otherwise.
 */
export async function handleSaveHuman(sessionId, humanId, humanData) {
	const Data = { sessionId, humanId, ...humanData };
	const url = baseURL + (humanId ? '/Human/UpdateHuman?' : '/Human/AddHuman?');
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);

	// Ensure the request was successful
	if (!response || response.Status !== 'Success') {
		console.error("Failed to save human:", response);
		return false;
	}

	return true;
}
