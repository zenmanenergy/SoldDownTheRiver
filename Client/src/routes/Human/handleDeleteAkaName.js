const baseURL = 'http://192.168.1.182';


export async function handleDeleteAkaName(AKAHumanId, HumanId) {
    const response = await fetch(`${baseURL}/Human/DeleteAKAName?AKAHumanId=${AKAHumanId}`);
    if (!response.ok) {
      const err = await response.json();
      console.error(err.message);
    }
    else {
      window.location.href = '/Human?HumanId=' + HumanId + '&tab=AKANames';
    }
  }
  