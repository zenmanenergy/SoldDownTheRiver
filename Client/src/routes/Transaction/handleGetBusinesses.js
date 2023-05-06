import { baseURL } from '../Settings';

export async function handleGetBusinesses(SessionId,callback) {
  const url=`${baseURL}/Transaction/GetBusinesses?SessionId=${SessionId}`
  console.log(url)
  const response = await fetch(url);
  const businesses = await response.json();
  callback(businesses);

}