// src/routes/Transactions/handleGet.js
import { baseURL } from '../Settings';
export async function handleSaveTransactionHuman(SessionId,TransactionId, HumanId,Price,Notes, callback) {
	const Data = {
		SessionId:SessionId,
		TransactionId:TransactionId,
		HumanId:HumanId,
		Price:Price,
	};
	const url = baseURL + '/Transaction/SaveTransactionHuman?'; 
	const FormValid=true
	let FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = `/Transaction?TransactionId=${TransactionId}`;
}
