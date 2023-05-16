// src/routes/Locations/handleSave.js
import { baseURL } from '../Settings';
// src/routes/Locations/handleSave.js
export function handleSave(SessionId,Location, formValid) {

  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}

  Location.SessionId=SessionId
  

  const queryString = Object.keys(Location)
    .map(key => key + '=' + encodeURIComponent(Location[key]))
    .join('&');

  const url = baseURL + '/Location/SaveLocation?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Locations';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
