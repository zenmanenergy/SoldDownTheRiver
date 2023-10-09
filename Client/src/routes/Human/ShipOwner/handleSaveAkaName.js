import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleSaveAkaName(SessionId,AKAHumanId,HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAFormValid) {



	const Data = {
		AKAHumanId: AKAHumanId,
		HumanId: HumanId,
		AKAFirstName: AKAFirstName,
		AKAMiddleName: AKAMiddleName,
		AKALastName: AKALastName,
		SessionId: SessionId
	};
	const url = baseURL + '/Human/SaveHumanAKA?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKA';
}
