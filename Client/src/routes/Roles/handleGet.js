import { baseURL } from '../Settings';

async function handleGet(SessionId) {
  const url=`${baseURL}/Roles/GetRoles?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const roles = await response.json();
  return roles;
}

export default handleGet;
