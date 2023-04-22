const baseURL = 'http://192.168.1.182';

export async function handleGetPossiblePartners(HumanId,setPossiblePartners) {
    console.log(`${baseURL}/Human/GetPossiblePartners?HumanId=${HumanId}`)
    const response = await fetch(`${baseURL}/Human/GetPossiblePartners?HumanId=${HumanId}`);
    const possiblePartners = await response.json();
    setPossiblePartners(possiblePartners)
}


