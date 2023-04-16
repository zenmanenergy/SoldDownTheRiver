// src/routes/Humans/handleSave.js
export function handleSave(data) {
	console.log("abc");
	const { HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes, formValid } = data;

	if (!formValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return;
	}

	let port = "";
	if (window.location.port == "3000") {
		port = ":80";
	}
	var endpoint = window.location.protocol + "//" + window.location.hostname + port + "/q?command=" + JSON.stringify(command);
	console.log(endpoint);
	fetch(endpoint)
		.then((response) => response.json())
		.then((result) => {
			// console.log(result.data);
			location.href = "/trade3?type=" + type + "&tradeSearchId=" + result.data.tradeSearchId;
		});
	console.log("Saving human:", { HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes });
}
