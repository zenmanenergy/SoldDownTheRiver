import { SuperFetch } from '../SuperFetch.js';
import { baseURL } from '../Settings.js';

export async function handleGetBuyers(sessionId, callback) {
	try {
		const Data = {
			
		};
		const url = baseURL + '/Roles/GetBuyers?'; 
		const FormValid=true
		let data = await SuperFetch(url, Data, FormValid)

		callback(data);
	} catch (error) {
		console.error('Error fetching Buyers:', error);
		throw error;
	}
}
