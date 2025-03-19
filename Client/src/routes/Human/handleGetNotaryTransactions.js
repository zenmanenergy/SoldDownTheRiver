import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetNotaryTransactions(SessionId, HumanId) {
	const Data = {
		SessionId: SessionId,
		HumanId: HumanId
	};
	const url = `${baseURL}/Human/GetNotaryTransactions?`;
	const FormValid = true;
	
	try {
		const response = await SuperFetch(url, Data, FormValid);
		console.log('Full Response:', response); // Debugging information
		if (response) {
			return response; // Return the response directly
		} else {
			throw new Error('Failed to fetch notary transactions');
		}
	} catch (error) {
		console.error('Error fetching notary transactions:', error);
		return [];
	}
}
