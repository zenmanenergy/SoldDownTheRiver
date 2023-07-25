import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';


export async function handleDeleteAkaName(SessionId,AKAHumanId, HumanId) {
	
	const Data = {
		SessionId:SessionId,
		AKAHumanId:AKAHumanId
	};
	const url = baseURL + '/Humans/GetHumans?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKANames';
}
  