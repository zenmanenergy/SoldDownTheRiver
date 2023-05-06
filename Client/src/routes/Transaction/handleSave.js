import { baseURL } from '../Settings';

// src/routes/Transactions/handleSubmit.js
export function handleSave(SessionId,transactionId, transactionDate, fromBusinessId, toBusinessId, transactionType, notes, act, page, notaryBusinessId, volume, url,  formValid) {

  if (!formValid) {
    const invalidFields = document.querySelectorAll("input:invalid");
    if (invalidFields.length > 0) {
      invalidFields[0].focus();
    }
    return;
  }

  const transactionData = {
    TransactionId: transactionId,
    TransactionDate: transactionDate,
    FromBusinessId: fromBusinessId,
    ToBusinessId: toBusinessId,
    TransactionType: transactionType,
    Notes: notes,
    Act: act,
    Page: page,
    NotaryBusinessId: notaryBusinessId,
    Volume: volume,
    URL: url,
    SessionId: SessionId
  };

  const queryString = Object.keys(transactionData)
    .map(key => key + '=' + encodeURIComponent(transactionData[key]))
    .join('&');

  const saveUrl = baseURL + '/Transaction/SaveTransaction?' + queryString; 
  console.log(saveUrl)
  fetch(saveUrl, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    console.log("Save success", data);
    window.location.href = '/Transactions';
    // Handle the response data as needed
  })
  .catch(error => {
    console.error("save error", error);
    // Handle the error as needed
  });
}
