import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetFamilies(callback) {
	const Data = {};
	const url = `${baseURL}/Families/GetFamilies?`;
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);
	callback(data);
}
