const baseURL = 'http://192.168.1.182';


export async function handleDeletePartner(SessionId,PartnerHumanId, HumanId) {
    const url=`${baseURL}/Human/DeletePartner?HumanId=${HumanId}&PartnerHumanId=${PartnerHumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    if (!response.ok) {
      const err = await response.json();
      console.error(err.message);
    }
    else {
      window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKANames';
    }
  }
  