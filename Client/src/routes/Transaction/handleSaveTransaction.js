import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

/**
 * Save or update human data.
 * @param {string} SessionId - The session ID for authentication.
 * @param {string|null} humanId - The ID of the human being updated (null for new records).
 * @param {Object} humanData - The human data to save.
 * @returns {Promise<boolean>} - Returns true if successful, false otherwise.
 */
export async function saveHuman(SessionId, humanId, humanData) {
	// Convert inches to cm before saving
	humanData.Height_cm = humanData.Height_in ? (parseFloat(humanData.Height_in) * 2.54).toFixed(2) : null;

	// Convert Roles to an array
	humanData.Roles = humanData.Roles.split(',').map(role => role.trim());

	const Data = { SessionId, humanId, ...humanData };
	const url = baseURL + '/Human/SaveHuman?';  // ✅ Fixed endpoint
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);

	// Ensure the request was successful
	if (!response || !response.success) {  // ✅ Fixed success check
		console.error("Failed to save human:", response);
		return false;
	}

	return true;
}
