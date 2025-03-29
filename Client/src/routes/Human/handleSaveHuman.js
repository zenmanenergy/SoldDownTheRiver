import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

// Add a sanitization helper to convert null/undefined to empty strings
function sanitize(value) {
	return value == null ? "" : value;
}

/**
 * Save or update human data.
 * @param {string} SessionId - The session ID for authentication.
 * @param {string|null} humanId - The ID of the human being updated (null for new records).
 * @param {Object} humanData - The human data to save.
 * @returns {Promise<Object|boolean>} - Returns the response object with HumanId if successful, false otherwise.
 */
export async function saveHuman(SessionId, humanId, humanData) {
	// Convert inches to cm before saving
	humanData.Height_cm = humanData.Height_in ? (parseFloat(humanData.Height_in) * 2.54).toFixed(2) : null;

	// Include additional fields with sanitized values and new TransactionId/RoleId fields
	const Data = {
		SessionId: sanitize(SessionId),
		humanId: sanitize(humanId),
		...Object.fromEntries(
			Object.entries(humanData).map(([key, value]) => [key, sanitize(value)])
		),
		age_string: sanitize(humanData.age_string),
		BirthPlace: sanitize(humanData.BirthPlace),
		originCity: sanitize(humanData.originCity),
		physical_features: sanitize(humanData.physical_features),
		profession: sanitize(humanData.profession),
		mergedHumanId: sanitize(humanData.mergedHumanId),
		spouseHumanId: sanitize(humanData.spouseHumanId),
		TransactionId: sanitize(humanData.TransactionId),  // new field
		RoleId: sanitize(humanData.RoleId)                   // new field
	};

	const url = baseURL + '/Human/SaveHuman?';
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);

	// Ensure the request was successful
	return response && response.success ? { ...response, HumanId: response.HumanId } : false;
}
