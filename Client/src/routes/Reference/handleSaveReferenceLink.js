import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSaveReferenceLink({ ReferenceId = '', LinkId, TargetType = 'Voyage', URL = '', Notes = '' }, callback) {
	const Data = { ReferenceId, LinkId, TargetType, URL, Notes };
	const url = baseURL + '/References/AddReferenceLink?';
	const FormValid = true;
	const result = await SuperFetch(url, Data, FormValid);
	if (callback) callback(result);
	return result;
}
