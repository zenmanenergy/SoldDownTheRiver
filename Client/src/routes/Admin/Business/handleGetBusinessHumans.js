// src/routes/Businesses/handleGet.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';
// src/routes/Business/handleGet.js
export async function handleGetBusinessHumans(SessionId, BusinessId, callback) {

	const Data = {
		SessionId:SessionId
	};
	const url = `${baseURL}/Business/GetBusinessHumans?BusinessId=${BusinessId}&SessionId=${SessionId}`
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);

}