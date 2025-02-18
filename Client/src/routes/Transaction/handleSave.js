import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSave(SessionId,transactionId, transactionDate, fromBusinessId, toBusinessId, transactionType, notes, act, page, notaryBusinessId, volume, formValid) {


	const Data = {
		TransactionId: transactionId,
		TransactionDate: transactionDate,
		FromBusinessId: fromBusinessId,
		ToBusinessId: toBusinessId,
		TransactionType: transactionType,
		Notes: notes,
		Act: act,
		Page: page,
		NotaryBusinessId: notaryBusinessId,
		Volume: volume,
		SessionId: SessionId
	};

	
	const _url = baseURL + '/Transaction/SaveTransaction?'; 
	FormValid=true 
	let data = await SuperFetch(_url, Data, FormValid)

	window.location.href = '/Transactions';
}
