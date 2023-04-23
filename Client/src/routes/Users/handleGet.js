const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  const response = await fetch(`${baseURL}/Users/GetUsers?SessionId=${SessionId}`);
  console.log(`${baseURL}/Users/GetUsers`)
  const users = await response.json();
  return users;
}

export default handleGet;
