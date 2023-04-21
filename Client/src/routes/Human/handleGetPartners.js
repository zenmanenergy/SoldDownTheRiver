// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetPartners(HumanId, setPartners) {
  console.log(`${baseURL}/getPartners?HumanId=${HumanId}`)
  const response = await fetch(`${baseURL}/GetPartners?HumanId=${HumanId}`);
  const data = await response.json();

  setPartners(data);
}