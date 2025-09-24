import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetLocations(SessionId, callback) {
	const Data = {
		SessionId: SessionId
	};
	const url = baseURL + '/Locations/GetLocations?';
	const FormValid = true;
	let data = await SuperFetch(url, Data, FormValid);

	// Populate Address if blank, using Name > County > City > State
	data = data.map(loc => {
		if (!loc.Address || loc.Address === null || loc.Address.trim() === "") {
			const parts = [];
			if (loc.County) parts.push(loc.County);
			if (loc.City) parts.push(loc.City);
			if (loc.State) parts.push(loc.State);
			loc.Address = parts.join(", ");
		}
		return loc;
	});

	callback(data);
}

