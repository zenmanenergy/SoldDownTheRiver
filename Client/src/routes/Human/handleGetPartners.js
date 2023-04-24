// src/routes/Humans/handleGetAKA.js
const baseURL = 'http://192.168.1.182';

export async function handleGetPartners(SessionId,HumanId, setPartners) {
  const url=`${baseURL}/Human/GetPartners?HumanId=${HumanId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setPartners(data);
}