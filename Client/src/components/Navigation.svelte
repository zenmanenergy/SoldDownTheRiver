<!-- src/components/Navigation.svelte -->
<script>
	import { onMount } from 'svelte';
	import { Session } from '../routes/Session.js';

	let isLoggedIn = false;
	let userType = '';
	let isLoading = true;

	onMount(async () => {
		await checkSession();
	});

	async function checkSession() {
		// Check if user has session cookies
		const sessionId = getCookie('SessionId');
		const userTypeCookie = getCookie('UserType');
		
		if (sessionId && userTypeCookie) {
			// Verify the session is still valid
			try {
				await Session.handleSession();
				isLoggedIn = true;
				userType = Session.UserType || userTypeCookie;
			} catch (error) {
				console.error('Session verification failed:', error);
				isLoggedIn = false;
				userType = '';
			}
		} else {
			isLoggedIn = false;
			userType = '';
		}
		
		isLoading = false;
	}

	function getCookie(name) {
		if (typeof window !== 'undefined' && window.Cookies) {
			return window.Cookies.get(name);
		}
		return null;
	}

	async function handleLogout(event) {
		event.preventDefault();
		await Session.logout();
		isLoggedIn = false;
		userType = '';
	}

	// Toggle mobile menu
	let isMobileMenuOpen = false;
	function toggleMobileMenu() {
		isMobileMenuOpen = !isMobileMenuOpen;
	}
</script>

{#if !isLoading}
	<div class="navmargin">
		<nav class="navbar is-link" aria-label="main navigation">
			<div class="navbar-brand">
				<button 
				   class="navbar-burger {isMobileMenuOpen ? 'is-active' : ''}" 
				   aria-label="menu" 
				   aria-expanded={isMobileMenuOpen}
				   on:click={toggleMobileMenu}>
					<span aria-hidden="true"></span>
					<span aria-hidden="true"></span>
					<span aria-hidden="true"></span>
				</button>
			</div>

			<div class="navbar-menu {isMobileMenuOpen ? 'is-active' : ''}">
				{#if isLoggedIn}
					<!-- Logged-in menu -->
					<div class="navbar-start">
						<a class="navbar-item" href="/Admin/Humans">Humans</a>
						<a class="navbar-item" href="/Admin/Transactions">Transactions</a>
						<a class="navbar-item" href="/Admin/Locations">Locations</a>
						<a class="navbar-item" href="/Admin/Roles">Roles</a>
						<a class="navbar-item" href="/Admin/Voyages">Voyages</a>
						<a class="navbar-item" href="/Admin/Ships">Ships</a>
						<a class="navbar-item" href="/Admin/References">References</a>
						<div class="navbar-item has-dropdown is-hoverable">
							<span class="navbar-link">Merge</span>
							<div class="navbar-dropdown">
								<a class="navbar-item" href="/Admin/Merge/Humans">Humans</a>
							</div>
						</div>
						<a class="navbar-item" href="/Search">Search</a>
					</div>
					<div class="navbar-end">
						{#if userType === "Administrator"}
							<a class="navbar-item" href="/Admin/Users">Users</a>
						{/if}
						<a class="navbar-item" href="/Admin/Login" on:click={handleLogout}>Logout</a>
					</div>
				{:else}
					<!-- Not logged-in menu -->
					<div class="navbar-start">
						<a class="navbar-item" href="/">Home</a>
						<a class="navbar-item" href="/Search">Search</a>
					</div>
					<div class="navbar-end">
						<a class="navbar-item" href="/Admin/Login">Login</a>
					</div>
				{/if}
			</div>
		</nav>
	</div>
{/if}
