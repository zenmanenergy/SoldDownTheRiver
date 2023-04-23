// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetAKA(SessionId,HumanId, setAkaNames) {
  console.log(`${baseURL}/Human/GetAkaNames?HumanId=${HumanId}&SessionId=${SessionId}`)
  const response = await fetch(`${baseURL}/Human/GetAkaNames?HumanId=${HumanId}&SessionId=${SessionId}`);
  const data = await response.json();

  setAkaNames(data);
}