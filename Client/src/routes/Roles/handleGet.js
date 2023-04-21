const baseURL = 'http://192.168.1.182';

async function handleGet() {
  const response = await fetch(`${baseURL}/GetRoles`);
  const roles = await response.json();
  return roles;
}

export default handleGet;
