import { baseURL } from './Settings';
class session {
    SessionId = "";

    async handleSession() {
        // Add your session handling logic here
        console.log("Handling session...");
        this.GetSessionId();

        await this.VerifySession(function(results) {
            console.log("session verified!", results);
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
        console.log(url);
        try {
            const response = await fetch(url, {
                method: 'GET'
            });
            const _SessionId = await response.json();
            if (this.SessionId == _SessionId) {
                Cookies.set("SessionId", this.SessionId, { expires: 365 });
            } else {
                Cookies.remove("SessionId");
                window.location.href = '/Login?s=1';
            }
            callback(_SessionId);
        } catch (error) {
            console.error("save error", error);
            // Handle the error as needed
        }
    }

    GetSessionId() {
        const urlParams = new URLSearchParams(window.location.search);

        if (urlParams.get("SessionId")) {
            this.SessionId = urlParams.get("SessionId");
        } else if (Cookies.get("SessionId")) {
            this.SessionId = Cookies.get("SessionId");
        } else {
            this.SessionId = "";
            Cookies.set("previousLocation", location.href)
            console.log(Cookies.get("previousLocation"))
            location.href = "/Login?s=1";
        }
        return true;
    }
}

export const Session = new session();
