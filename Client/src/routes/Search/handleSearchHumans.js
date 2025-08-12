import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSearchHumans(callback) {
	const Data = {  };
	const url = baseURL + '/Humans/GetHumans?'; 
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	// Format the roles and also known as values, replace null values with empty strings
	const formattedData = data.map(human => {
		const hasNoName = !human.FirstName && !human.MiddleName && !human.LastName;
		return {
			...human, // Spread original human data
			FirstName: hasNoName ? 'Unnamed' : (human.FirstName || ''),
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
		};
	});

	callback(formattedData);
}
