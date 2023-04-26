// src/routes/Users/handleGet.js
import { baseURL } from '../Settings';
export async function handleGet(SessionId,UserId, setUser) {
    const url=`${baseURL}/User/GetUser?UserId=${UserId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
    setUser(data.FirstName, data.LastName, data.Email, data.Phone, data.Password, data.School, data.SemesterYear, data.UserType);
}
