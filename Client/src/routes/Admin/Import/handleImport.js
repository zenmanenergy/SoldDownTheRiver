import { baseURL } from '../../Settings';

export function handleImport(SessionId,SpreadsheetName, SpreadsheetData) {
  
  let postData={}
  postData.SessionId= SessionId
  postData.SpreadsheetName= SpreadsheetName
  postData.SpreadsheetData= SpreadsheetData

  postData = JSON.stringify(postData)
  const url = baseURL + '/Import/ImportData'; 
  console.log(url)
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: postData
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success",data);
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error",error);
    // Handle the error as needed
  });
}
