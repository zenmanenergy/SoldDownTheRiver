// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleSearch(SessionId, SearchButton) {
    let url = `${baseURL}/Search/${SearchButton.label}?`
    for(let i = 0; i<SearchButton.boxnames.length ; i++) {
        url += `${SearchButton.boxnames[i]}=${SearchButton.arg[i]}`
    }
    url += `&SessionId=${SessionId}`
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
  
}
  