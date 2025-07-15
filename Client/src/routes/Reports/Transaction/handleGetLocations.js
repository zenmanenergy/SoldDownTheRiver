import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetLocations(callback) {
	const Data = {
	};
	const url = baseURL + '/Locations/GetLocations?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);

}

