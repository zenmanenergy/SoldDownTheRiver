const baseURL = 'http://192.168.1.182';

export async function handleGet(SessionId,HumanId, setHumanName) {
    console.log(`${baseURL}/Human/GetHuman?HumanId=${HumanId}&SessionId=${SessionId}`)
    const response = await fetch(`${baseURL}/Human/GetHuman?HumanId=${HumanId}&SessionId=${SessionId}`);
    const data = await response.json();
  
    const { FirstName, MiddleName, LastName , StartYear, EndYear, Notes, RoleId} = data;
    // const humanName = `${FirstName} ${MiddleName} ${LastName}`.trim();
  
    setHumanName(FirstName, MiddleName, LastName, StartYear, EndYear, Notes, RoleId);
}
