import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

// src/routes/Businesses/handleSubmit.js
export async function handleSave(SessionId,BusinessId, BusinessName, LocationId, FormValid) {
	console.log("handlesave")

	const Data = {
		BusinessId: BusinessId,
		BusinessName: BusinessName,
		SessionId: SessionId,
		LocationId: LocationId
	};
	
	const url = `${baseURL}/Business/SaveBusiness?`
	FormValid=true
	let data = await SuperFetch(url, Data, FormValid)
	window.location.href = '/Businesses';


	// if (!FormValid) {
	// 	const invalidFields = document.querySelectorAll("input:invalid");
	// 	if (invalidFields.length > 0) {
	// 		invalidFields[0].focus();
	// 	}
	// 	return;
	// }
	// const businessData = {
	// 	BusinessId: BusinessId,
	// 	BusinessName: BusinessName,
	// 	SessionId: SessionId,
	// 	LocationId: LocationId
	// };

	// const queryString = Object.keys(businessData)
	// 	.map(key => key + '=' + encodeURIComponent(businessData[key]))
	// 	.join('&');

	// const url = baseURL + '/Business/SaveBusiness?' + queryString; 
	// console.log(url)
	// fetch(url, {
	// 	method: 'GET'
	// })
	// .then(response => response.json())
	// .then(data => {
	// 	console.log("Save success",data);
	// 	window.location.href = '/Businesses';
	// 	// Handle the response data as needed
	// })
	// .catch(error => {
	// 	console.error("save error",error);
	// 	// Handle the error as needed
	// });
}
