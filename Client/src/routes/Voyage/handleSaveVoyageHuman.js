
import { baseURL } from '../Settings';
export async function handleSaveVoyageHuman(SessionId,VoyageId, HumanId, VoyageHumanRoleId, VoyageHumanNotes, callback) {

	const Data = {
		SessionId:SessionId,
		VoyageId:VoyageId,
		HumanId:HumanId,
		VoyageHumanRoleId:VoyageHumanRoleId,
		VoyageHumanNotes:VoyageHumanNotes
	};
	const url = baseURL + '/Voyage/SaveVoyageHuman?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
