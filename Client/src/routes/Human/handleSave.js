import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSave(SessionId,HumanId, FirstName, MiddleName, LastName,	Notes, RoleId,formValid ) {

	const Data = {
		HumanId: HumanId,
		FirstName: FirstName,
		MiddleName: MiddleName,
		LastName: LastName,
		Notes: Notes,
		SessionId: SessionId,
		RoleId:RoleId
	};
	console.log("Data",Data)
	const url = baseURL + '/Human/SaveHuman?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	// window.location.href = '/Role/?RoleId='+RoleId;
	
}
