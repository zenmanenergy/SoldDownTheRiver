import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

// src/routes/Users/handleSave.js
export async function handleSave(SessionId,userId, firstName, lastName, email, phone, password, school, semesterYear,UserType, FormValid) {

	const Data = {
		UserId: userId,
		FirstName: firstName,
		LastName: lastName,
		Email: email,
		Phone: phone,
		Password: password,
		School: school,
		SemesterYear: semesterYear,
		UserType: UserType,
		SessionId: SessionId
	};
	const url = baseURL + '/User/SaveUser?'; 
	let data = await SuperFetch(url, Data, FormValid)

	window.location.href = '/Users';
}
