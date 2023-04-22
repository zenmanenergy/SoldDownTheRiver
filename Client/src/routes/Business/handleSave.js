const baseURL = 'http://192.168.1.182';

// src/routes/Businesses/handleSubmit.js
export function handleSave(businessId, BusinessName,formValid) {

  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}
  const businessData = {
    BusinessId: businessId,
    BusinessName: BusinessName
  };

  const queryString = Object.keys(businessData)
    .map(key => key + '=' + encodeURIComponent(businessData[key]))
    .join('&');

  const url = baseURL + '/Business/SaveBusiness?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Businesses';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
