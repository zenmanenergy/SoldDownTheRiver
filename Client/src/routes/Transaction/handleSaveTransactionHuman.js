import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSaveTransactionHuman(SessionId, TransactionId, human) {
	const Data = {
		SessionId: SessionId,
		TransactionId: TransactionId,
		HumanId: human.HumanId || "", // Send empty string if no ID
		FirstName: human.FirstName,
		LastName: human.LastName,
		RacialDescriptor: human.RacialDescriptor,
		Sex: human.Sex,
		Height_cm: human.Height_cm,
		physical_features: human.physical_features,
		profession: human.profession,
		BirthPlace: human.BirthPlace,
		AgeYears: human.AgeYears,
		AgeMonths: human.AgeMonths,
		BirthDate: human.BirthDate,
		BirthDateAccuracy: human.BirthDateAccuracy,
		Price: human.Price,
		Notes: human.Notes || "",
	};

	const url = baseURL + '/Transaction/SaveTransactionHuman?';
	const FormValid = true;
	
	// Send request and wait for server response
	let response = await SuperFetch(url, Data, FormValid);

	// Return the updated human data from the server
	return response;
}
