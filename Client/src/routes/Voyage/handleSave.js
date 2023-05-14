import { baseURL } from '../Settings';

export function handleSave(SessionId,Voyage,formValid) {

  console.log('handleSave', Voyage);
  console.log(formValid)
  if (!formValid) {
    const invalidFields = document.querySelectorAll('input:invalid');
    if (invalidFields.length > 0) {
      invalidFields[0].focus();
    }
    return;
  }
console.log('handleSave', Voyage, formValid);
  if (Voyage.StartDate instanceof Date) {
    Voyage.StartDate = Voyage.StartDate.toISOString();
  } else {
    Voyage.StartDate = "";
  }
  if (Voyage.EndDate instanceof Date) {
    Voyage.EndDate = Voyage.EndDate.toISOString();
  } else {
    Voyage.EndDate = "";
  }
    Voyage.SessionId= SessionId 

  const queryString = Object.keys(Voyage)
    .map((key) => key + '=' + encodeURIComponent(Voyage[key]))
    .join('&');

  const url = baseURL + '/Voyage/SaveVoyage?' + queryString;
  console.log(url);
  fetch(url, {
    method: 'GET',
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Save success', data);
      window.location.href = '/Voyages';
      // Handle the response data as needed
    })
    .catch((error) => {
      console.error('Save error', error);
      // Handle the error as needed
    });
}
