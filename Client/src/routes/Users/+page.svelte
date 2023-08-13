<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetUsers } from './handleGetUsers.js';
	import { Session } from "../Session.js";

	export let Users = [];
	let filteredUsers = [];
	let isLoading = true;
	let searchQuery = '';

	async function setUsers(data) {
		Users = data;
	}

	onMount(async () => {
		await Session.handleSession();
		await Promise.all([
			handleGetUsers(Session.SessionId, setUsers),
		]);
		isLoading = false;
	});

	$: filteredUsers = Users.filter(user => {
		const fullName = `${user.FirstName} ${user.LastName}`.toLowerCase();
		return fullName.includes(searchQuery.toLowerCase());
	});

	function addUser() {
		window.location.href = '/User?UserId=';
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/AdminMenu">Back to Menu</a>
		<div class="ActionBox">
			<h3 class="title is-2">List of Users</h3>
			<button on:click={addUser}>Add User</button>
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by  name" />
					</div>
			
				</div>
			</form>
			<ul>
				{#each filteredUsers as user}
					<li>
						<a href={`/User?UserId=${user.UserId}`}>
							{user.FirstName} {user.LastName}
						</a>
					</li>
				{/each}
			</ul>
			<button on:click={addUser}>Add User</button>
		</div>
	</div>
{/if}
