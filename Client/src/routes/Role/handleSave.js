const baseURL = 'http://192.168.1.182';

// src/routes/Roles/handleSave.js
export function handleSave(RoleId,Role, formValid) {

  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}
  const roleData = {
    RoleId: RoleId,
    Role: Role
  };

  const queryString = Object.keys(roleData)
    .map(key => key + '=' + encodeURIComponent(roleData[key]))
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
