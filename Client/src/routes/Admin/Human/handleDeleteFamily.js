import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';


export async function handleDeleteFamily(SessionId,FamilyHumanId, HumanId) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId,
		FamilyHumanId:FamilyHumanId
	};
	const url = baseURL + '/Human/DeleteFamily?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Admin/Human?HumanId=' + HumanId + '&tab=AKANames';
}
	