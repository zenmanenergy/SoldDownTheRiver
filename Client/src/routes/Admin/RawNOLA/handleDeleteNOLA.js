import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleDeleteNOLA(SessionId, NOLA_ID) {
	const Data = {
		SessionId: SessionId,
		NOLA_ID: NOLA_ID
	};
	const url = baseURL + '/RawNOLA/DeleteRawNOLA?';

	let result = await SuperFetch(url, Data, true);
	alert(result.message);
	window.location.href = "/Admin/RawNOLAs";
}
