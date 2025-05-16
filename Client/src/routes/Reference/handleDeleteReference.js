import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleDeleteReference(SessionId, ReferenceId) {
	const Data = { SessionId, ReferenceId };
	const url = baseURL + '/References/DeleteReference?';
	const FormValid = true;

	let result = await SuperFetch(url, Data, FormValid);

	if (!result) {
		return { success: false, error: 'No response from server.' };
	}
	if (result.error) {
		return { success: false, error: result.error };
	}
	return { success: true };
}
