import { SuperFetch } from '../SuperFetch.js';
import { baseURL } from '../Settings.js';

export async function handleGetCollectorAgents(sessionId, callback) {
	try {
		const Data = {
			
		};
		const url = baseURL + '/Roles/GetCollectorAgents?'; 
		const FormValid=true
		let data = await SuperFetch(url, Data, FormValid)

		callback(data);
	} catch (error) {
		console.error('Error fetching CollectorAgents:', error);
		throw error;
	}
}
