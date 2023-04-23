const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  console.log(`${baseURL}/Roles/GetRoles?SessionId=${SessionId}`)
  const response = await fetch(`${baseURL}/Roles/GetRoles?SessionId=${SessionId}`);
  const roles = await response.json();
  return roles;
}

export default handleGet;
