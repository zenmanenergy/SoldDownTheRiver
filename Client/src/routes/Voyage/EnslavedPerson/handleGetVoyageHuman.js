import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetVoyageHuman(SessionId, VoyageId, HumanId, callback) {
	const Data = {
		SessionId:SessionId,
		VoyageId:VoyageId,
		HumanId:HumanId
	};
	const url = baseURL + '/Voyage/EnslavedPerson/GetVoyageHuman?'; 
	const FormValid=true
	console.log("DataDataData",Data)
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
