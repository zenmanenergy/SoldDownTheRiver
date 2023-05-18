import { baseURL } from '../Settings';

export async function handleGetRoles(SessionId, dallback) {
  const url=`${baseURL}/Voyage/GetRoles?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const roles = await response.json();
  dallback(roles);
}
