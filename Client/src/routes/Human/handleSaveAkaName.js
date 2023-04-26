import { baseURL } from '../Settings';

export function handleSaveAkaName(SessionId,AKAHumanId,HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAFormValid) {

  if (!AKAFormValid) {
    const invalidFields = document.querySelectorAll("input:invalid");
    if (invalidFields.length > 0) {
      invalidFields[0].focus();
    }
    return;
  }
  console.log('valid')
  const AKAHumanData = {
    AKAHumanId: AKAHumanId,
    HumanId: HumanId,
    AKAFirstName: AKAFirstName,
    AKAMiddleName: AKAMiddleName,
    AKALastName: AKALastName,
    SessionId: SessionId
  };

  console.log('AKAHumanData',AKAHumanData)
  const queryString = Object.keys(AKAHumanData)
    .map(key => key + '=' + encodeURIComponent(AKAHumanData[key]))
    .join('&');

  const url = baseURL + '/Human/SaveHumanAKA?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKA';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
