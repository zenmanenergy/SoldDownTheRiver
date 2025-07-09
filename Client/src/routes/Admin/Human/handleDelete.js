import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleDelete(SessionId,HumanId) {
	

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Human/DeleteHuman?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Admin/Humans';

}
