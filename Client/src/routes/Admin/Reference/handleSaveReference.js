import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleSaveReference(SessionId, refData) {
	const Data = {
		SessionId,
		ReferenceId: refData.ReferenceId,
		URL: refData.URL,
		Notes: refData.Notes
	};
	const url = baseURL + '/References/SaveReference?';
	const FormValid = true;

	let result = await SuperFetch(url, Data, FormValid);

	if (!result) {
		return { success: false, error: 'No response from server.' };
	}
	if (result.error) {
		return { success: false, error: result.error };
	}
	return { success: true, ReferenceId: result.ReferenceId };
}
