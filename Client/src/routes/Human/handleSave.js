const baseURL = 'http://192.168.1.182';

export function handleSave(HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes, RoleId, formValid ) {

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
    StartYear: StartYear,
    EndYear: EndYear,
    Notes: Notes,
    RoleId: RoleId
  };

  console.log('humanData',humanData)
  const queryString = Object.keys(humanData)
    .map(key => key + '=' + encodeURIComponent(humanData[key]))
    .join('&');

	console.log('queryString',queryString)
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
