import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSaveTransactionHuman(SessionId, TransactionId, HumanId,RoleId) {
	const Data = {
		SessionId: SessionId,
		TransactionId: TransactionId,
		HumanId: HumanId || "",
		RoleId: RoleId || ""
	};

	const url = baseURL + '/Transaction/SaveTransactionHuman?';
	const FormValid = true;
	
	// Send request and wait for server response
	let response = await SuperFetch(url, Data, FormValid);

	// Return the updated human data from the server
	return response;
}
