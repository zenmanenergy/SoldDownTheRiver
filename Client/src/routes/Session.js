import { baseURL } from './Settings';

class session {
	SessionId = "";
	UserType = "";

	async logout() {
		console.log("Handling logout...");
		if (typeof window !== 'undefined' && window.Cookies) {
			window.Cookies.remove("SessionId");
			window.Cookies.remove("UserType");
		}
		window.location.href = '/Admin/Login?s=1';
	}

	async handleSession() {
		console.log("Handling session...");
		this.GetSessionId();
		console.log("After GetSessionId, SessionId is:", this.SessionId);

		await this.VerifySession((results) => {
			if (results && results.SessionId && results.UserType) {
				console.log("Session verified successfully!", results);
				if (typeof window !== 'undefined' && window.Cookies) {
					window.Cookies.set("SessionId", results.SessionId, { expires: 365 });
					window.Cookies.set("UserType", results.UserType, { expires: 365 });
				}
				this.UserType = results.UserType;
			} else {
				console.log("Session verification failed, logging out...");
				this.logout();
			}
		});
	}

	async VerifySession(callback) {
		const VerifySessionData = {
			SessionId: this.SessionId
		};

		const queryString = Object.keys(VerifySessionData)
			.map(key => key + '=' + encodeURIComponent(VerifySessionData[key]))
			.join('&');

		const url = baseURL + '/Login/Verify?' + queryString;
		console.log("Verifying session with URL:", url);
		console.log("SessionId being verified:", this.SessionId);
		try {
			const response = await fetch(url, { method: 'GET' });
			console.log("Verify response status:", response.status);
			const data = await response.json();
			console.log("Verify response data:", data);
			if (data && data.SessionId && data.UserType) {
				console.log("Session verification successful");
				callback(data);
			} else {
				console.log("Session verification failed - no valid data returned");
				callback(null);
			}
		} catch (error) {
			console.error("Verify session error:", error);
			callback(null);
		}
	}

	GetSessionId() {
		const urlParams = new URLSearchParams(window.location.search);

		if (urlParams.get("SessionId")) {
			this.SessionId = urlParams.get("SessionId");
			console.log("SessionId found in URL params:", this.SessionId);
		} else if (typeof window !== 'undefined' && window.Cookies && window.Cookies.get("SessionId")) {
			this.SessionId = window.Cookies.get("SessionId");
			console.log("SessionId found in cookies:", this.SessionId);
		} else {
			console.log("No SessionId found, redirecting to login");
			this.SessionId = "";
			if (typeof window !== 'undefined' && window.Cookies) {
				window.Cookies.set("previousLocation", location.href);
			}
			if (typeof window !== 'undefined') {
				location.href = "/Admin/Login?s=1";
			}
		}
		return true;
	}
}

export const Session = new session();
