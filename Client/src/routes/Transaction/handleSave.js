import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSave(SessionId,transactionId, transactionDate, fromBusinessId, toBusinessId, transactionType, notes, act, page, notaryBusinessId, volume, url,	formValid) {


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
		URL: url,
		SessionId: SessionId
	};

	
	const url = baseURL + '/Transaction/SaveTransaction?'; 
	FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Transactions';
}
