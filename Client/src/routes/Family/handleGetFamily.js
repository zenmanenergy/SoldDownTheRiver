import { baseURL } from '../Settings.js';
import { SuperFetch } from '../SuperFetch.js'; // Ensure the correct relative path and file extension

export async function handleGetFamily(SessionId,HumanId, callback) {
	const Data = {
		SessionId:SessionId,
		HumanId: HumanId
	};
	const url = `${baseURL}/Family/GetFamily?`;
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);
	// Format the roles properly and replace null values with empty strings
	const formattedData = data.map(FamilyMember => ({
		...FamilyMember, // Spread original FamilyMember data
		FirstName: FamilyMember.FirstName || '',
		LastName: FamilyMember.LastName || '',
		SpouseFirstName: FamilyMember.SpouseFirstName || '',
		SpouseLastName: FamilyMember.SpouseLastName || '',
		left_value: FamilyMember.left_value || '',
		right_value: FamilyMember.right_value || ''
	}));
	callback(formattedData);
}
