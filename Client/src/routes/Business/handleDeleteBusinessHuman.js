
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDeleteBusinessHuman(SessionId, BusinessId, HumanId) {

	const Data = {
		SessionId:SessionId
	};
	const url=`${baseURL}/Business/DeleteBusinessHuman?BusinessId=${BusinessId}&HumanId=${HumanId}&SessionId=${SessionId}`
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = `/Business?BusinessId=${BusinessId}`;
}
