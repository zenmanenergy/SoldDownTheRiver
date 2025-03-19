<style>
	@import '/static/FormPages.css';
	
	/* Add styles for row hover effect */
	tbody tr:hover {
		background-color: #444444; /* or any other color you like */
		cursor: pointer;
	}
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
		console.log(Users)
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
		
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-2">List of Users</h3>
				<button class="button is-primary" on:click={addUser}>Add User</button>
			</div>
			<div class="field">
				<div class="control">
					<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" />
				</div>
			</div>
			<div class="table-container">
				<table class="table is-striped is-fullwidth">
					<thead>
						<tr>
							<th>Name</th>
							<th>Email</th>
							<th>Phone Number</th>
						</tr>
					</thead>
					<tbody>
						{#each filteredUsers as user}
							<tr on:click={() => window.location.href = `/User?UserId=${user.UserId}`}>
								<td>{user.FirstName || 'unknown'} {user.LastName || 'unknown'}</td>
								<td>{user.Email || 'unknown'}</td>
								<td>{user.Phone || 'unknown'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
{/if}
