import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetSlaveShippingAgents(SessionId, callback) {
	const Data = {
		
	};
	const url = baseURL + '/Voyage/GetSlaveShippingAgents?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
