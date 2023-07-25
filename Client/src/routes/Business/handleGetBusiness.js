import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetBusiness(SessionId, BusinessId, callback) {
	

	const Data = {
		SessionId:SessionId
	};
	const url = `${baseURL}/Business/GetBusiness?BusinessId=${BusinessId}&SessionId=${SessionId}`
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
  