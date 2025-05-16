import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSaveVoyageHuman(VoyageId, Human,callback) {

	const Data= {
		VoyageId:VoyageId,
		HumanId: Human.HumanId,
		RoleId: Human.RoleId,
		owner_humanid: Human.owner_humanid || '',
		owner2_humanid: Human.owner2_humanid || '',
		shippingagent_humanid: Human.shippingagent_humanid || '',
		collectoragent_HumanId: Human.collectoragent_humanid || '',
		Notes: Human.Notes || ''
	};
	const url = baseURL + '/Voyage/SaveVoyageHuman?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}
