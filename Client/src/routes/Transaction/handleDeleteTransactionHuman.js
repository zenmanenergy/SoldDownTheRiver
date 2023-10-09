
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleDeleteTransactionHuman(SessionId,TransactionId,HumanId) {
	

	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Transaction/DeleteTransactionHuman?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = `/Transaction?TransactionId=${TransactionId}`;
}
