const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  const url="${baseURL}/Roles/GetRoles?SessionId=${SessionId}"
  console.log(url)
  const response = await fetch(url);
  const roles = await response.json();
  return roles;
}

export default handleGet;
