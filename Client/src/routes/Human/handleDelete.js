const baseURL = 'http://192.168.1.182';

export async function handleDelete(SessionId,HumanId) {
  try {
    console.log(`${baseURL}/Human/DeleteHuman?HumanId=${HumanId}&SessionId=${SessionId}`)
    const response = await fetch(`${baseURL}/Human/DeleteHuman?HumanId=${HumanId}&SessionId=${SessionId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log(`Human with ID ${HumanId} has been deleted.`);
    window.location.href = '/Humans';
  } catch (error) {
    console.error('There was a problem deleting the human:', error);
  }
}
