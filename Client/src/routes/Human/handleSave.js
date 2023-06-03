import { baseURL } from '../Settings';

export function handleSave(SessionId,HumanId, FirstName, MiddleName, LastName,  Notes, RoleId, formValid ) {

  if (!formValid) {
    const invalidFields = document.querySelectorAll("input:invalid");
    if (invalidFields.length > 0) {
      invalidFields[0].focus();
    }
    return;
  }
  console.log('valid')
  const humanData = {
    HumanId: HumanId,
    FirstName: FirstName,
    MiddleName: MiddleName,
    LastName: LastName,
    
    Notes: Notes,
    RoleId: RoleId,
    SessionId: SessionId
  };

  console.log('humanData',humanData)
  const queryString = Object.keys(humanData)
    .map(key => key + '=' + encodeURIComponent(humanData[key]))
    .join('&');

  const url = baseURL + '/Human/SaveHuman?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Humans';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
