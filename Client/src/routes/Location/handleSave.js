
import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';
export async function handleSave(SessionId,Data, FormValid) {

	Data.SessionId=SessionId
	const url = baseURL + '/Location/SaveLocation?'; 
	FormValid=true 
	let data = await SuperFetch(url, Data, FormValid)
	window.location.href = '/Locations';
}
