import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetHumanVoyages(HumanId) {
	const Data = {
		HumanId: HumanId
	};
	const url = `${baseURL}/Human/GetVoyages?`;
	const FormValid = true;

	try {
		const response = await SuperFetch(url, Data, FormValid);
		// console.log('Full Response:', response); // Debugging information
		if (response) {
			return response; // Return the response directly
		} else {
			throw new Error('Failed to fetch human voyages');
		}
	} catch (error) {
		console.error('Error fetching human voyages:', error);
		return [];
	}
}
