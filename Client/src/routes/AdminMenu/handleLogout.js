import { baseURL } from '../Settings';

export function handleLogout() {
  
	Cookies.remove("sessionId");
	
	window.location.href = '/Login?s=1';
}
