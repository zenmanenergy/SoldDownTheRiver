import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch.js'; // Ensure the correct relative path and file extension

export async function handleFamilyTree(HumanId, callback) {
	const Data = {
		HumanId: HumanId
	};
	const url = `${baseURL}/Family/GetFamily?`;
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);
	callback(data);
}
