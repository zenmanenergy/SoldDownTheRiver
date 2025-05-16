import { SuperFetch } from '../SuperFetch.js';
import { baseURL } from '../Settings.js';

export async function handleGetSellers(sessionId, callback) {
	try {
		const Data = {
			
		};
		const url = baseURL + '/Roles/GetSellers?'; 
		const FormValid=true
		let data = await SuperFetch(url, Data, FormValid)

		callback(data);
	} catch (error) {
		console.error('Error fetching sellers:', error);
		throw error;
	}
}
