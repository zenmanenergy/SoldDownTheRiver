const baseURL = 'http://192.168.1.182';

export function handleSavePartner(SessionId,HumanId, PartnerHumanId) {

  console.log('valid')
  const PartnerData = {
    HumanId: HumanId,
    PartnerHumanId: PartnerHumanId,
    SessionId: SessionId
  };

  console.log('PartnerData',PartnerData)
  const queryString = Object.keys(PartnerData)
    .map(key => key + '=' + encodeURIComponent(PartnerData[key]))
    .join('&');

	console.log('queryString',queryString)
  const url = baseURL + '/Human/SavePartner?' + queryString; 
  console.log(url)
  fetch(url, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    window.location.href = '/Human?HumanId=' + HumanId + '&tab=Partners';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
