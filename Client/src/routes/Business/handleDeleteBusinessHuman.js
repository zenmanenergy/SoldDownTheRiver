
import { baseURL } from '../Settings';
export async function handleDeleteBusinessHuman(SessionId, BusinessId, HumanId) {
  
    const url=`${baseURL}/Business/DeleteBusinessHuman?BusinessId=${BusinessId}&HumanId=${HumanId}&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    
    const data = await response.json();
    window.location.href = `/Business?BusinessId=${BusinessId}`;

    
}
