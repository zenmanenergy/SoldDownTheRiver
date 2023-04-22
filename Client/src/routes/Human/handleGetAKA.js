// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetAKA(HumanId, setAkaNames) {
  console.log(`${baseURL}/Human/GetAkaNames?HumanId=${HumanId}`)
  const response = await fetch(`${baseURL}/Human/GetAkaNames?HumanId=${HumanId}`);
  const data = await response.json();

  setAkaNames(data);
}