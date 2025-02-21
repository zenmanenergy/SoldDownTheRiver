import { baseURL } from '../Settings';
import { SuperFetch } from '../SuperFetch';

export async function handleLogin(Email, Password, formValid, callback) {
	console.log("handleLogin", Email, Password, formValid);

	// Check if form is valid before proceeding
	if (!formValid) {
		console.log("Form is invalid");
		const invalidFields = document.querySelectorAll("input:invalid");
		if (invalidFields.length > 0) {
			const firstInvalidField = invalidFields[0];
			if (firstInvalidField) {
				firstInvalidField.focus();
			}
		}
		callback(false);
		return false;
	}

	// Create login data
	const LoginData = {
		Email: Email,
		Password: Password
	};

	// Convert to query string
	const queryString = Object.keys(LoginData)
		.map(key => key + '=' + encodeURIComponent(LoginData[key]))
		.join('&');

	const url = `${baseURL}/Login/Login?${queryString}`;
	console.log("Login URL:", url);

	try {
		const response = await fetch(url, { method: 'GET' });
		const SessionId = await response.json();

		// Handle successful login
		if (SessionId) {
			console.log("Login successful, SessionId:", SessionId);
			Cookies.set("SessionId", SessionId, { expires: 365 });

			// Redirect to previous location if available
			const previousLocation = Cookies.get("previousLocation");
			if (previousLocation) {
				window.location.href = previousLocation;
			} else {
				callback(true);
				window.location.href = "/?s=0";
			}
		} else {
			console.error("Invalid login response, no SessionId received");
			Cookies.remove("SessionId"); // Fix: Ensure correct cookie casing

			// Focus on the first input field (Email)
			// const formFields = document.querySelectorAll("input");
			// if (formFields.length > 0) {
			// 	formFields[0].focus();
			// }

			callback(false);
		}
	} catch (error) {
		console.error("Login error:", error);

		// Show error message
		const serverErrorElement = document.getElementById("ServerError");
		if (serverErrorElement) {
			serverErrorElement.innerHTML = `<p style="color: red;">Login failed: ${error.message}</p>`;
			serverErrorElement.style.visibility = "visible";
			serverErrorElement.style.display = "block";
		}

		callback(false);
	}

	return true;
}
