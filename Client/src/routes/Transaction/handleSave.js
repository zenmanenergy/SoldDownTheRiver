const baseURL = 'http://192.168.1.182';

// src/routes/Transactions/handleSubmit.js
export function handleSave(SessionId,transactionId, transactionDate, fromHumanId, toHumanId, transactionType, notes, act, page, notaryHumanId, volume, url, userId, formValid) {

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
    FromHumanId: fromHumanId,
    ToHumanId: toHumanId,
    TransactionType: transactionType,
    Notes: notes,
    Act: act,
    Page: page,
    NotaryHumanId: notaryHumanId,
    Volume: volume,
    URL: url,
    UserId: userId,
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
