import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleSearchTransactions(callback) {
	const Data = {};
	const url = baseURL + '/Transactions/GetSearchTransactions?'; 
	const FormValid = true;

	let data = await SuperFetch(url, Data, FormValid);

	// Ensure the response is valid
	if (!data || !Array.isArray(data)) {
		console.error("Invalid data received from API:", data);
		callback([]);
		return;
	}

	// Format the data, replace null values with empty strings
	const formattedData = data.map(transaction => ({
		...transaction, // Spread original transaction data
		TransactionId: transaction.TransactionId || '',
		TransactionType: transaction.TransactionType || '',
		date_circa: transaction.date_circa || '',
		date_accuracy: transaction.date_accuracy || '',
		TotalPrice: transaction.TotalPrice || '',
		Act: transaction.Act || '',
		Page: transaction.Page || '',
		Volume: transaction.Volume || '',
		URL: transaction.URL || '',
		LocationId: transaction.LocationId || '',
		LocationAddress: transaction.LocationAddress || '',
		LocationCity: transaction.LocationCity || '',
		LocationCounty: transaction.LocationCounty || '',
		LocationStateAbbr: transaction.LocationStateAbbr || '',
		Buyers: transaction.Buyers || '',
		Sellers: transaction.Sellers || '',
		Notary: transaction.Notary || ''
	}));
	
	callback(formattedData);
}

