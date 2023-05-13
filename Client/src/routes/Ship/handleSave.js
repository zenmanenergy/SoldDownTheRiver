import { baseURL } from '../Settings';

// src/routes/Ships/handleSave.js
export function handleSave(SessionId, ShipData, formValid) {
  console.log("handleSave", SessionId, ShipData, formValid)
  if (!formValid) {
    const invalidFields = document.querySelectorAll("input:invalid");
    if (invalidFields.length > 0) {
      invalidFields[0].focus();
    }
    return;
  }
  console.log("valide", SessionId, ShipData, formValid)
  ShipData.SessionId = SessionId;
  if (ShipData.BuildDate instanceof Date) {
    ShipData.BuildDate = ShipData.BuildDate.toISOString();
  } else {
    ShipData.BuildDate = "";
  }
  const queryString = Object.keys(ShipData)
    .map(key => key + '=' + encodeURIComponent(ShipData[key]))
    .join('&');

  const url = baseURL + '/Ship/SaveShip?' + queryString;
  console.log(url);

  fetch(url, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(data => {
      console.log("Save success", data);
      window.location.href = '/Ships';
      // Handle the response data as needed
    })
    .catch(error => {
      console.error("Save error", error);
      // Handle the error as needed
    });
}
