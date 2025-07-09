import { baseURL } from '../Settings';

export function handleLogout() {
  
	Cookies.remove("SessionId");
	
	window.location.href = '/Login?s=1';
}
