import { baseURL } from '../Settings';

export async function handleGetPossibleFamilys(SessionId,HumanId,setPossibleFamily) {
    const url=`${baseURL}/Human/GetPossibleFamilys?HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const possibleFamilys = await response.json();
    setPossibleFamily(possibleFamilys)
}


