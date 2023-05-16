import { baseURL } from '../Settings';

// src/routes/Roles/handleSave.js
export function handleSave(SessionId,Role, formValid) {
  console.log("handleSave",SessionId,Role, formValid)
  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}
  Role.SessionId= SessionId

  const queryString = Object.keys(Role)
    .map(key => key + '=' + encodeURIComponent(Role[key]))
    .join('&');

  const url = baseURL + '/Role/SaveRole?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Roles';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
