// src/routes/Humans/handleGetAKA.js
import { baseURL } from '../Settings';

export async function handleGetPartners(SessionId,HumanId, setPartners) {
  const url=`${baseURL}/Human/GetPartners?HumanId=${HumanId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setPartners(data);
}