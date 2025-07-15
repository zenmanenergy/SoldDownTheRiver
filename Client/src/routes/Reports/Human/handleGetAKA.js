import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetAKA(HumanId, callback) {
	

	const Data = {
		HumanId:HumanId
	};
	const url = baseURL + '/Human/GetAkaNames?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}