// src/routes/Locations/handleSave.js
const baseURL = 'http://192.168.1.182';
// src/routes/Locations/handleSave.js
export function handleSave(SessionId,locationId, city, state, country, latitude, longitude, formValid) {

  if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}

  const locationData = {
    LocationId: locationId,
    City: city,
    State: state,
    Country: country,
    Latitude: latitude,
    Longitude: longitude,
    SessionId: SessionId

  };

  const queryString = Object.keys(locationData)
    .map(key => key + '=' + encodeURIComponent(locationData[key]))
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
