import { baseURL } from '../Settings';

export async function handleGetPossibleFamilies(SessionId,HumanId,setPossibleFamily) {
    const url=`${baseURL}/Human/GetPossibleFamilies?HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const possibleFamilies = await response.json();
    setPossibleFamily(possibleFamilies)
}


