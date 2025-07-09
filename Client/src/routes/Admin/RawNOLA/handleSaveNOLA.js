import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

export async function handleSaveNOLA(SessionId, NOLA, formValid) {

	const Data = {
		SessionId: SessionId,
		NOLA_ID: NOLA.NOLA_ID,
		FirstParty: NOLA.FirstParty,
		LocationFirstParty: NOLA.LocationFirstParty,
		SecondParty: NOLA.SecondParty,
		LocationSecondParty: NOLA.LocationSecondParty,
		TypeOfTransaction: NOLA.TypeOfTransaction,
		DateOfTransaction: NOLA.DateOfTransaction,
		Act: NOLA.Act,
		Page: NOLA.Page,
		NotaryPublic: NOLA.NotaryPublic,
		Volume: NOLA.Volume,
		NameOfTranscriber: NOLA.NameOfTranscriber,
		ReferenceURL: NOLA.ReferenceURL
	};

	const url = baseURL + '/RawNOLA/SaveRawNOLA?';
	let result = await SuperFetch(url, Data, formValid);

	alert(result.message);
}
