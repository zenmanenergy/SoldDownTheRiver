import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetSlaveCollectingAgents(SessionId, callback) {
	const Data = {
		
	};
	const url = baseURL + '/Voyage/GetSlaveCollectingAgents?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
