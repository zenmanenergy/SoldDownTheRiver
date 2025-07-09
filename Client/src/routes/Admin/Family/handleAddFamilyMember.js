import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleAddFamilyMember(SessionId, HumanId, RelatedHumanId, RelationshipType) {
	const Data = {
		SessionId,
		HumanId,
		RelatedHumanId,
		RelationshipType
	};
	const url = baseURL + '/Family/AddFamilyMember?';
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);

	if (response && response.success) {
		return true;
	} else {
		console.error("Failed to add family members:", response);
		return false;
	}
}
