import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetTransactions(ShipId,callback) {

	const Data = {
		ShipId:ShipId,
	}
	const url = baseURL + '/Ship/GetTransactions?'
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
