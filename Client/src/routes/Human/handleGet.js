const baseURL = 'http://192.168.1.182';

export async function handleGet(HumanId, setHumanName) {
    console.log(`${baseURL}/Human/GetHuman?HumanId=${HumanId}`)
    const response = await fetch(`${baseURL}/Human/GetHuman?HumanId=${HumanId}`);
    const data = await response.json();
  
    const { FirstName, MiddleName, LastName , StartYear, EndYear, Notes, RoleId} = data;
    // const humanName = `${FirstName} ${MiddleName} ${LastName}`.trim();
  
    setHumanName(FirstName, MiddleName, LastName, StartYear, EndYear, Notes, RoleId);
}
