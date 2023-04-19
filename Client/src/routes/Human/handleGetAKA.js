// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetAKA(HumanId, setAkaNames) {
  console.log(`${baseURL}/GetAkaNames?HumanId=${HumanId}`)
  const response = await fetch(`${baseURL}/GetAkaNames?HumanId=${HumanId}`);
  const data = await response.json();

  setAkaNames(data);
}