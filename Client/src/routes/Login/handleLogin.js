const baseURL = 'http://192.168.1.182';

// src/routes/Businesses/handleSubmit.js
export function handleLogin(Email, Password,formValid) {
  console.log("handleLogin",Email, Password,formValid)

  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}
  const LoginData = {
    Email: Email,
    Password: Password
  };

  const queryString = Object.keys(LoginData)
    .map(key => key + '=' + encodeURIComponent(LoginData[key]))
    .join('&');

  const url = baseURL + '/Login/Login?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/AdminMenu';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
