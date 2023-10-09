import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetLocations(SessionId, callback) {
	console.log("getlocations")
	const Data = {
		SessionId:SessionId
	};
	const url=`${baseURL}/Business/GetLocations?SessionId=${SessionId}`
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}

