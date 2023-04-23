const baseURL = 'http://192.168.1.182';


export async function handleDeletePartner(SessionId,PartnerHumanId, HumanId) {
    console.log(`${baseURL}/Human/DeletePartner?HumanId=${HumanId}&PartnerHumanId=${PartnerHumanId}&SessionId=${SessionId}`)
    const response = await fetch(`${baseURL}/Human/DeletePartner?HumanId=${HumanId}&PartnerHumanId=${PartnerHumanId}&SessionId=${SessionId}`);
    if (!response.ok) {
      const err = await response.json();
      console.error(err.message);
    }
    else {
      window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKANames';
    }
  }
  