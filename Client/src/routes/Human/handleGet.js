const baseURL = 'http://192.168.1.182';

export async function handleGet(HumanId, setHumanName) {
    const response = await fetch(`${baseURL}/GetHuman?HumanId=${HumanId}`);
    const data = await response.json();
  
    const { FirstName, MiddleName, LastName , StartYear, EndYear, Notes} = data;
    // const humanName = `${FirstName} ${MiddleName} ${LastName}`.trim();
  
    setHumanName(FirstName, MiddleName, LastName, StartYear, EndYear, Notes);
}
