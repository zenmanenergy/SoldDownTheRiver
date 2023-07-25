
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDeleteVoyageHuman(SessionId,VoyageId,HumanId) {

	const Data = {
		SessionId:SessionId,
		VoyageId:VoyageId,
		HumanId:HumanId
	};
	const url = baseURL + '/Voyage/DeleteVoyageHuman?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = `/Voyage?VoyageId=${VoyageId}`;
}
