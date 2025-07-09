// src/routes/Businesses/handleGet.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';
// src/routes/Business/handleGet.js
export async function handleGetHumans(SessionId,callback) {
	const Data = {
		SessionId:SessionId
	};
	const url = `${baseURL}/Business/GetHumans?SessionId=${SessionId}`
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}