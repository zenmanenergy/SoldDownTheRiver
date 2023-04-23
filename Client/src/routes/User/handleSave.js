const baseURL = 'http://192.168.1.182';

// src/routes/Users/handleSave.js
export function handleSave(SessionId,userId, firstName, lastName, email, phone, password, school, semesterYear,UserType, formValid) {

  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}
  const userData = {
    UserId: userId,
    FirstName: firstName,
    LastName: lastName,
    Email: email,
    Phone: phone,
    Password: password,
    School: school,
    SemesterYear: semesterYear,
    UserType: UserType,
    SessionId: SessionId
  };

  const queryString = Object.keys(userData)
    .map(key => key + '=' + encodeURIComponent(userData[key]))
    .join('&');

  const url = baseURL + '/User/SaveUser?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Users';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
