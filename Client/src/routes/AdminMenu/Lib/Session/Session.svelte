<script>
    export let _sessionId="";
	let sessionVerified=false;
    export const sessionId = function(){
		return _sessionId
	}
    export const handleSession= function (){
		if (urlParams.get("sessionId") && !sessionVerified){
        	_sessionId = urlParams.get("sessionId");
			console.log("URL SESSION ID")
			verifySession(function(results){
				console.log("session verified!",results);
				console.log(results.method)
				if (results.method=="sessionVerified"){
					sessionVerified=true
					Cookies.set("sessionId",_sessionId,{expires: 7});
				}
			});
			
		}else if (Cookies.get("sessionId")){
			console.log("COOKIE SESSION ID")
			_sessionId=Cookies.get("sessionId");
		}else{
			console.log("NO SESSION ID")
			location.href="/login?s=1";
			return false;
		}
		return true
	}
	export const verifySession=function(onSuccess){
		
		let command={}
		command.object="users"
		command.method="verifyBySessionId";
		command.data={};
		command.data.sessionId=_sessionId;

		let port="";
        if (window.location.port=="3000"){
            port=":80";
        }
        var endpoint=window.location.protocol+"//" + window.location.hostname +port+"/q?command="+JSON.stringify(command);
		console.log(endpoint)
		fetch(endpoint).then((response) => response.json()).then((results) => {
			console.log(results)
			// handleLogout(results)
			onSuccess(results)
		})
		.catch((error)=>{

			console.log(error)
			//location.href="/error";
		});
	}
	export const verifyAdminSession=function(onSuccess){
		handleSession()
		let command={}
		command.object="admin"
		command.method="verifyAdminSession";
		command.data={};
		command.data.sessionId=_sessionId;

		let port="";
        if (window.location.port=="3000"){
            port=":80";
        }
        var endpoint=window.location.protocol+"//" + window.location.hostname +port+"/q?command="+JSON.stringify(command);
		console.log(endpoint)
		fetch(endpoint).then((response) => response.json()).then((results) => {
			console.log(results)
			// handleLogout(results)
			onSuccess(_sessionId)
		})
		.catch((error)=>{

			console.log(error)
			//location.href="/error";
		});
	}
	export const handleLogout=function(results){
		if (results.method=="serverGo"){
			console.log("S2")
			location.href="/"+results.data.id+"?s=2"
			return false;
		}
		if (results.method=="missingVariables"){
			console.log(results)
			console.log("S3")
			location.href="/login?s=3";
			return false;
		}
		return true
	}
</script>