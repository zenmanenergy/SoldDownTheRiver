import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleDelete(SessionId, VoyageId) {

	const Data = {
		SessionId:SessionId,
		VoyageId:VoyageId
	};
	const url = baseURL + '/Voyage/DeleteVoyage?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Voyages';
}
