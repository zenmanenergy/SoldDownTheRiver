import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleGetEnslavedTransactions(SessionId, HumanId) {
	const Data = {
		SessionId: SessionId,
		HumanId: HumanId
	};
	const url = `${baseURL}/Human/GetEnslavedTransactions?`;
	const FormValid = true;
	
	try {
		const response = await SuperFetch(url, Data, FormValid);
		console.log('Full Response:', response); // Debugging information
		if (response) {
			return response; // Return the response directly
		} else {
			throw new Error('Failed to fetch enslaved transactions');
		}
	} catch (error) {
		console.error('Error fetching enslaved transactions:', error);
		return [];
	}
}
