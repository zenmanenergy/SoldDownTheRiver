const baseURL = 'http://192.168.1.182';

async function handleGet() {
  const response = await fetch(`${baseURL}/Users/GetUsers`);
  console.log(`${baseURL}/Users/GetUsers`)
  const users = await response.json();
  return users;
}

export default handleGet;
