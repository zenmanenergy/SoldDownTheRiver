const baseURL = 'http://192.168.1.182';

async function handleGet() {
  const response = await fetch(`${baseURL}/GetHumans`);
  const Humans = await response.json();
  return Humans;
}

export default handleGet;