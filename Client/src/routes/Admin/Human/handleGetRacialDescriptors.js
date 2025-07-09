import { SuperFetch } from '../../SuperFetch.js';
import { baseURL } from '../../Settings.js';

export async function handleGetRacialDescriptors(sessionId) {
	try {
		const url = `${baseURL}/Humans/GetRacialDescriptors?SessionId=${sessionId}`;
		const result = await SuperFetch(url, {}, true);
		return result || [];
	} catch (error) {
		console.error('Error fetching racial descriptors:', error);
		return [];
	}
}
