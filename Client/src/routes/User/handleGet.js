// src/routes/Users/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGet(UserId, setUser) {
    const response = await fetch(`${baseURL}/GetUser?UserId=${UserId}`);
    console.log(`${baseURL}/GetUser?UserId=${UserId}`)
    const data = await response.json();
  
    setUser(data.FirstName, data.LastName, data.Email, data.Phone, data.Password, data.School, data.SemesterYear);
}
