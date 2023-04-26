import { baseURL } from '../Settings';

export async function handleGetPossiblePartners(SessionId,HumanId,setPossiblePartners) {
    const url=`${baseURL}/Human/GetPossiblePartners?HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const possiblePartners = await response.json();
    setPossiblePartners(possiblePartners)
}


