
import { baseURL } from '../Settings';
export async function handleSaveVoyageHuman(SessionId,VoyageId, HumanId,callback) {
  
  const url=`${baseURL}/Voyage/SaveVoyageHuman?VoyageId=${VoyageId}&HumanId=${HumanId}&SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const data = await response.json();
  callback(data[0]);
  window.location.href = `/Voyage?VoyageId=${VoyageId}`;
}
