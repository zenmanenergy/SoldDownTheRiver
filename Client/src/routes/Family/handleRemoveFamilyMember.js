import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleRemoveFamilyMember(SessionId, HumanId, RelatedHumanId) {
	const Data = {
		SessionId,
		HumanId,
		RelatedHumanId
	};
	const url = baseURL + '/Family/RemoveFamilyMember?';
	const FormValid = true;

	let response = await SuperFetch(url, Data, FormValid);

	if (response && response.success) {
		return true;
	} else {
		console.error("Failed to add family members:", response);
		return false;
	}
}
