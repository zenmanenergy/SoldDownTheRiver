// src/routes/Users/handleDelete.js
import { baseURL } from '../Settings';
export async function handleDelete(SessionId,UserId) {
	try {
		const url = `${baseURL}/User/DeleteUser?UserId=${UserId}&SessionId=${SessionId}`;
		console.log(url);
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		console.log(`User with ID ${UserId} has been deleted.`);
		window.location.href = "/Users";
	} catch (error) {
		console.error("There was a problem deleting the user:", error);
	}
}
