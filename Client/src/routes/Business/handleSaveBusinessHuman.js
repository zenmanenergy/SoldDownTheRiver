// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
// src/routes/Business/handleGet.js
export async function handleSaveBusinessHuman(SessionId, BusinessId, HumanId, RoleId) {

	const Data = {
		SessionId:SessionId
	};
	const url = `${baseURL}/Business/SaveBusinessHuman?BusinessId=${BusinessId}&HumanId=${HumanId}&RoleId=${RoleId}&SessionId=${SessionId}`
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)
	window.location.href = `/Business?BusinessId=${BusinessId}`;

}
  