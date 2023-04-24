// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetAKA(SessionId,HumanId, setAkaNames) {
  const url="${baseURL}/Human/GetAkaNames?HumanId=${HumanId}&SessionId=${SessionId}"
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setAkaNames(data);
}