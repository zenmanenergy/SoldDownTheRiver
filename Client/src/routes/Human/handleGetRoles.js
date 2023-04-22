// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetRoles(setRoles) {
  console.log(`${baseURL}/Human/GetRoles`)
  const response = await fetch(`${baseURL}/Human/GetRoles`);
  const data = await response.json();

  setRoles(data);
}