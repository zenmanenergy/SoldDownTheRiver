const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  const response = await fetch(`${baseURL}/Humans/GetHumans?SessionId=${SessionId}`);
  const Humans = await response.json();
  return Humans;
}

export default handleGet;