import { baseURL } from '../Settings';

export async function handleGet(SessionId,HumanId, setHumanName) {
    const url=`${baseURL}/Human/GetHuman?HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    const { FirstName, MiddleName, LastName , StartYear, EndYear, Notes, RoleId} = data;
    // const humanName = `${FirstName} ${MiddleName} ${LastName}`.trim();
  
    if (HumanId){
        setHumanName(FirstName, MiddleName, LastName, StartYear, EndYear, Notes, RoleId);
    }
}
