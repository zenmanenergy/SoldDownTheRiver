const baseURL = 'http://192.168.1.182';

export async function handleDelete(SessionId,HumanId) {
  try {
    const url="${baseURL}/Human/DeleteHuman?HumanId=${HumanId}&SessionId=${SessionId}"
    console.log(url)
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Human with ID ${HumanId} has been deleted.`);
    window.location.href = '/Humans';
  } catch (error) {
    console.error('There was a problem deleting the human:', error);
  }
}
