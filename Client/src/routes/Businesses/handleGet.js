import { baseURL } from '../Settings';

export async function handleGet(SessionId, callback) {
  const url=`${baseURL}/Businesses/GetBusinesses?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const businesses = await response.json();
  callback(businesses);
}
