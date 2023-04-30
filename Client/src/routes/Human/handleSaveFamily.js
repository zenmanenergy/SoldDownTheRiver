import { baseURL } from '../Settings';

export function handleSaveFamily(SessionId,HumanId, FamilyHumanId, Relationship) {

  console.log('valid')
  const FamilyData = {
    HumanId: HumanId,
    FamilyHumanId: FamilyHumanId,
    SessionId: SessionId,
    Relationship:Relationship
  };

  console.log('FamilyData',FamilyData)
  const queryString = Object.keys(FamilyData)
    .map(key => key + '=' + encodeURIComponent(FamilyData[key]))
    .join('&');

	console.log('queryString',queryString)
  const url = baseURL + '/Human/SaveFamily?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Human?HumanId=' + HumanId + '&tab=Familys';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
