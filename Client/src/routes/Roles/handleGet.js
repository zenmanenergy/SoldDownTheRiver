const baseURL = 'http://192.168.1.182';

async function handleGet() {
  console.log(`${baseURL}/Roles/GetRoles`)
  const response = await fetch(`${baseURL}/Roles/GetRoles`);
  const roles = await response.json();
  return roles;
}

export default handleGet;
