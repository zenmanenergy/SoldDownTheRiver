const baseURL = 'http://192.168.1.182';

async function handleGet(SessionId) {
  const url="${baseURL}/Humans/GetHumans?SessionId=${SessionId}"
  console.log(url)
  const response = await fetch(url);
  const Humans = await response.json();
  return Humans;
}

export default handleGet;