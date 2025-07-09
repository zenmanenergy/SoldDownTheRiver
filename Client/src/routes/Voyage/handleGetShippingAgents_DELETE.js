import { SuperFetch } from '../SuperFetch.js';
import { baseURL } from '../Settings.js';

export async function handleGetShippingAgents(sessionId, callback) {
	try {
		const Data = {
			
		};
		const url = baseURL + '/Roles/GetShippingAgents?'; 
		const FormValid=true
		let data = await SuperFetch(url, Data, FormValid)

		callback(data);
	} catch (error) {
		console.error('Error fetching ShippingAgents:', error);
		throw error;
	}
}
