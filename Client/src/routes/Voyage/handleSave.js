import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSave(SessionId,Data,FormValid) {

	// if (Data.StartDate instanceof Date) {
	// 	Data.StartDate = Data.StartDate.toISOString();
	// } else {
	// 	Data.StartDate = "";
	// }
	// if (Data.EndDate instanceof Date) {
	// 	Data.EndDate = Data.EndDate.toISOString();
	// } else {
	// 	Data.EndDate = "";
	// }
		Data.SessionId= SessionId 

	

	const url = baseURL + '/Voyage/SaveVoyage?'; 
	FormValid=true 
	console.log(Data)
	let data = await SuperFetch(url, Data, FormValid)

	// callback(data);
	// window.location.href = '/Voyages';
}
