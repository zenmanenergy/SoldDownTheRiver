// src/routes/Users/handleDelete.js
const baseURL = "http://192.168.1.182";
export async function handleDelete(SessionId,UserId) {
	try {
		const response = await fetch(`${baseURL}/User/DeleteUser?UserId=${UserId}&SessionId=${SessionId}`);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		console.log(`User with ID ${UserId} has been deleted.`);
		window.location.href = "/Users";
	} catch (error) {
		console.error("There was a problem deleting the user:", error);
	}
}
