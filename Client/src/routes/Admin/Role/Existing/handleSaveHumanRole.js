import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleSaveHumanRole(SessionId,RoleId, HumanId,callback) {

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId,
		RoleId:RoleId
	}
	const url = baseURL + '/Role/SaveHumanRole?'
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Admin/Role?RoleId='+RoleId;
}
