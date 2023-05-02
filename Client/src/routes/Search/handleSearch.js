// src/routes/Businesses/handleGet.js
import { baseURL } from '../Settings';
// src/routes/Business/handleGet.js
export async function handleSearch(SessionId, SearchButton, setData) {
    let url = `${baseURL}/Search/${SearchButton.label}?SessionId=${SessionId}`
    for(let i = 0; i<SearchButton.boxnames.length ; i++) {
        url += `&${SearchButton.boxnames[i]}=${SearchButton.arg[i]}`
    }
    console.log(url)
    const response = await fetch(url);
    const data = await response.json();
    setData(data)
}
  