import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

// Add a sanitization helper to convert null/undefined to empty strings
function sanitize(value) {
	return value == null ? "" : value;
}

/**
 * Save or update timeline data.
 * @param {string} sessionId - The session ID for authentication.
 * @param {string|null} humanId - The ID of the human (null for new records).
 * @param {Object} timelineData - The timeline data to save.
 * @returns {Promise<Object|boolean>} - Response object if successful, false otherwise.
 */
export async function handleSaveTimeline(sessionId, humanId, timelineData) {
	// Spread the timelineData so each property becomes a query parameter,
	// and use "HumanId" (uppercase) for the human id.
	const Data = {
		SessionId: sanitize(sessionId),
		HumanId: sanitize(humanId),
		...timelineData
	};

	const url = baseURL + '/Human/SaveTimeline?'; // mimic style using SuperFetch
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);
	return response && response.success ? { ...response, TimelineId: response.TimelineId } : false;
}
