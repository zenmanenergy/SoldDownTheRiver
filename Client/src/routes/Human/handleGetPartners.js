// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetPartners(SessionId,HumanId, setPartners) {
  console.log(`${baseURL}/Human/GetPartners?HumanId=${HumanId}&SessionId=${SessionId}`)
  const response = await fetch(`${baseURL}/Human/GetPartners?HumanId=${HumanId}&SessionId=${SessionId}`);
  const data = await response.json();

  setPartners(data);
}