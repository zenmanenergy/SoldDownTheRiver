import { baseURL } from '../Settings';

export async function handleGet(SessionId, dallback) {
  const url=`${baseURL}/Roles/GetRoles?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const roles = await response.json();
  dallback(roles);
}
