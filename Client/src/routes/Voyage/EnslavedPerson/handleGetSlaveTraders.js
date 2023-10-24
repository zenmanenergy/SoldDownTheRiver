import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetSlaveTraders(SessionId, callback) {
	const Data = {
		
	};
	const url = baseURL + '/Voyage/GetSlaveTraders?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
