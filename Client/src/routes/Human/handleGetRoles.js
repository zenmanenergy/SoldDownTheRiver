import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetRoles(SessionId) {
	const Data = {
		SessionId: SessionId
	};
	const url = baseURL + '/Human/GetRoles?';
	const FormValid = true;
	let data = await SuperFetch(url, Data, FormValid);
	return data;
}