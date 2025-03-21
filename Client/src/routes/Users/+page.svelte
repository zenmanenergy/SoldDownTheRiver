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
	let sortColumn = 'FirstName';
	let sortAscending = true;

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

	$: filteredUsers = [...filteredUsers].sort((a, b) => {
		let valueA = a[sortColumn] ?? '';
		let valueB = b[sortColumn] ?? '';

		// Convert to lowercase for case-insensitive sorting
		if (typeof valueA === 'string') valueA = valueA.toLowerCase();
		if (typeof valueB === 'string') valueB = valueB.toLowerCase();

		if (valueA < valueB) return sortAscending ? -1 : 1;
		if (valueA > valueB) return sortAscending ? 1 : -1;
		return 0;
	});

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

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
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('FirstName')}>Name</th>
							<th on:click={() => toggleSort('Email')}>Email</th>
							<th on:click={() => toggleSort('Phone')}>Phone Number</th>
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
