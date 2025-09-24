// src/routes/Humans/handleGetAKA.js
import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleGetFamilies(SessionId,HumanId, callback) {

	const Data = {
		SessionId:SessionId,
		HumanId:HumanId
	};
	const url = baseURL + '/Family/GetFamily?'; 
	const FormValid=true
	let data = await SuperFetch(url, Data, FormValid)

	callback(data);
}