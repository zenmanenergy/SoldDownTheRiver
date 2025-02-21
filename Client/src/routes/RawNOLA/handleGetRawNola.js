import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetRawNola(SessionId,callback) {
	const Data = {
		SessionId:SessionId
	};
	const url = baseURL + '/RawNOLA/GetRawNOLA?SessionId?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}

