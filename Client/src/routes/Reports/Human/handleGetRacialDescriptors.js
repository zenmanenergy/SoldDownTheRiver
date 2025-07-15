import { SuperFetch } from '../../SuperFetch.js';
import { baseURL } from '../../Settings.js';

export async function handleGetRacialDescriptors() {
	try {
		const url = `${baseURL}/Humans/GetRacialDescriptors?`;
		const result = await SuperFetch(url, {}, true);
		return result || [];
	} catch (error) {
		console.error('Error fetching racial descriptors:', error);
		return [];
	}
}
