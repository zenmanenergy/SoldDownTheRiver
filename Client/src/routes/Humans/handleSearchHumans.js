import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSearchHumans(SessionId, Query, callback) {
	const Data = { SessionId, Query };
	const url = baseURL + '/Humans/SearchHumans?';
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	const formattedData = data.map(human => ({
		...human,
		FirstName: human.FirstName || '',
		MiddleName: human.MiddleName || '',
		LastName: human.LastName || '',
		isCompany: human.isCompany || '',
		BirthDate: human.BirthDate || '',
		BirthDateAccuracy: human.BirthDateAccuracy || '',
		RacialDescriptor: human.RacialDescriptor || '',
		Sex: human.Sex || '',
		Height_in: human.Height_in || '',
		Roles: human.Roles ? human.Roles.split(', ') : [],
		AlsoKnownAs: human.AlsoKnownAs ? human.AlsoKnownAs.split(', ') : []
	}));

	callback(formattedData);
}
