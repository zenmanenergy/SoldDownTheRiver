import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetHumanTransactions(SessionId, HumanId) {
	const Data = {
		SessionId: SessionId,
		HumanId: HumanId
	};
	const url = `${baseURL}/Human/GetHumanTransactions?`;
	const FormValid = true;
	
	try {
		const response = await SuperFetch(url, Data, FormValid);
		console.log('Full Response:', response); // Debugging information
		if (response) {
			return response; // Return the response directly
		} else {
			throw new Error('Failed to fetch human transactions');
		}
	} catch (error) {
		console.error('Error fetching human transactions:', error);
		return [];
	}
}
