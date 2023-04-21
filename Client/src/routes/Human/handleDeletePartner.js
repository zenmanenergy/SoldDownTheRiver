const baseURL = 'http://192.168.1.182';


export async function handleDeletePartner(PartnerHumanId, HumanId) {
    console.log(`${baseURL}/DeletePartner?HumanId=${HumanId}&PartnerHumanId=${PartnerHumanId}`)
    const response = await fetch(`${baseURL}/DeletePartner?HumanId=${HumanId}&PartnerHumanId=${PartnerHumanId}`);
    if (!response.ok) {
      const err = await response.json();
      console.error(err.message);
    }
    else {
      window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKANames';
    }
  }
  