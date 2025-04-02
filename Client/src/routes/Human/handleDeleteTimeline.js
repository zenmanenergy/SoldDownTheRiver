import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

function sanitize(value) {
	return value == null ? "" : value;
}

/**
 * Delete a timeline entry.
 * @param {string} sessionId - The session ID for authentication.
 * @param {string|null} humanId - The human's ID.
 * @param {string} locationId - The unique ID of the timeline entry (LocationId).
 * @returns {Promise<Object|boolean>} - Returns the response if successful, false otherwise.
 */
export async function handleDeleteTimeline(sessionId, humanId, locationId) {
	const Data = {
		SessionId: sanitize(sessionId),
		HumanId: sanitize(humanId),
		LocationId: sanitize(locationId)
	};

	const url = baseURL + '/Human/DeleteTimeline?';
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);
	return response && response.success ? response : false;
}
