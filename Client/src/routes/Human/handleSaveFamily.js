import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSaveFamily(SessionId,HumanId, FamilyHumanId, Relationship) {



	const Data = {
		HumanId: HumanId,
		FamilyHumanId: FamilyHumanId,
		SessionId: SessionId,
		Relationship:Relationship
	};
	const url = baseURL + '/Humans/SaveFamily?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Human?HumanId=' + HumanId + '&tab=Families';
}
