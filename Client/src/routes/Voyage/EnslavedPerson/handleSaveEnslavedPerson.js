import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleSaveEnslavedPerson(SessionId, EnslavedPersonData, FormValid) {
	
	EnslavedPersonData.SessionId = SessionId;
	
	const url = baseURL + '/Voyage/EnslavedPerson/SaveEnslavedPerson?'; 
	let data = await SuperFetch(url, EnslavedPersonData, FormValid)

	window.location.href = '/Ships';
}
