const baseURL = 'http://192.168.1.182';

export function handleSaveAkaName(AKAHumanId,HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAFormValid) {

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
    AKALastName: AKALastName
  };

  console.log('AKAHumanData',AKAHumanData)
  const queryString = Object.keys(AKAHumanData)
    .map(key => key + '=' + encodeURIComponent(AKAHumanData[key]))
    .join('&');

	console.log('queryString',queryString)
  const url = baseURL + '/SaveHumanAKA?' + queryString; 
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
