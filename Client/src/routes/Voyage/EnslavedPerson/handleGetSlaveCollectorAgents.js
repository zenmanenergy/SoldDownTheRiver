import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetSlaveCollectorAgents(SessionId, callback) {
	const Data = {
		
	};
	const url = baseURL + '/Voyage/GetSlaveCollectorAgents?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
