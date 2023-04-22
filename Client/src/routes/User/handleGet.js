// src/routes/Users/handleGet.js
const baseURL = 'http://192.168.1.182';
export async function handleGet(UserId, setUser) {
    console.log(`${baseURL}/User/GetUser?UserId=${UserId}`)
    const response = await fetch(`${baseURL}/User/GetUser?UserId=${UserId}`);
    const data = await response.json();
  
    setUser(data.FirstName, data.LastName, data.Email, data.Phone, data.Password, data.School, data.SemesterYear);
}
