import { baseURL } from './Settings';

export function handleLogout() {
  
	Cookies.remove("SessionId");
	Cookies.remove("UserRole");
	console.log("logout")
	window.location.href = '/Login?s=1';
}
