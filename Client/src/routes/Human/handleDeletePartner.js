const baseURL = 'http://192.168.1.182';


export async function handleDeletePartner(PartnerHumanId, HumanId) {
    const response = await fetch(`${baseURL}/DeletePartner?PartnerHumanId=${PartnerHumanId}`);
    if (!response.ok) {
      const err = await response.json();
      console.error(err.message);
    }
    else {
      window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKANames';
    }
  }
  