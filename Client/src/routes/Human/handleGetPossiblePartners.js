const baseURL = 'http://192.168.1.182';

export async function handleGetPossiblePartners(SessionId,HumanId,setPossiblePartners) {
    console.log(`${baseURL}/Human/GetPossiblePartners?HumanId=${HumanId}&SessionId=${SessionId}`)
    const response = await fetch(`${baseURL}/Human/GetPossiblePartners?HumanId=${HumanId}&SessionId=${SessionId}`);
    const possiblePartners = await response.json();
    setPossiblePartners(possiblePartners)
}


