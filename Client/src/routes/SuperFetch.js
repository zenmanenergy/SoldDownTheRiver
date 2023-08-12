

export async function SuperFetch(url, Data, FormValid){
	if (!FormValid) {
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			invalidFields[0].focus();
		}
		return true;
	}
	

	const queryString = Object.keys(Data)
		.map(key => key + '=' + encodeURIComponent(Data[key]))
		.join('&');

	url += queryString
	console.log(url)
	let results;
	try {
		const response = await fetch(url);
		results = await response.json();
		if (results.ErrorMessage){
			console.error("uh oh!", results.ErrorMessage+"\n\n"+results.StackTrace)
			throw(results.ErrorMessage+"\n\n"+results.StackTrace)
		}
	} catch (error) {
		document.getElementById("ServerURL").innerHTML="<a target='_blank' href='"+url+"'>"+url+"</a>"
		document.getElementById("ServerErrorMessage").innerHTML="<xmp>"+error+"</xmp>"
		document.getElementById("ServerError").style.visibility="";
		document.getElementById("ServerError").style.display="block";
		return False
	}
	return results
}