import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetRawNolas(SessionId,callback) {
	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/RawNOLA/GetRawNOLAs?SessionId?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}

