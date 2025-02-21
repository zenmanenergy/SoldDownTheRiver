export const baseURL = (() => {
	if (typeof window !== 'undefined') {
		return window.location.hostname === '127.0.0.1'
			? 'http://127.0.0.1:9000'
			: 'https://api.solddownriver.com';
	}
	return 'https://api.solddownriver.com'; // Default for static builds
})();
