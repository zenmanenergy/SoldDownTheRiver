import { baseURL } from './Settings';

export function handleLogout() {
  
	if (typeof window !== 'undefined' && window.Cookies) {
		window.Cookies.remove("SessionId");
		window.Cookies.remove("UserRole");
	}
	console.log("logout")
	window.location.href = '/Admin/Login?s=1';
}
