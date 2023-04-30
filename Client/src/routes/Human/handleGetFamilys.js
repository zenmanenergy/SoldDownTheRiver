// src/routes/Humans/handleGetAKA.js
import { baseURL } from '../Settings';

export async function handleGetFamilys(SessionId,HumanId, setFamily) {
  const url=`${baseURL}/Human/GetFamilys?HumanId=${HumanId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();

  setFamily(data);
}