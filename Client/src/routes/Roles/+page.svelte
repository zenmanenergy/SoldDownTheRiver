<style>
	@import '/static/FormPages.css';
</style>

<script>
	import { onMount } from 'svelte';
	import { handleGetRoles } from './handleGetRoles.js';
	import { Session } from "../Session.js";

	export let Roles = [];
	let isLoading = true;
	let sortColumn = 'Role';
	let sortAscending = true;

	async function setRoles(data) {
		Roles = data;
	}

	onMount(async () => {
		await Session.handleSession();
		await handleGetRoles(Session.SessionId, setRoles);
		isLoading = false;
	});

	function addRole() {
		window.location.href = '/Role?RoleId=';
	}

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	$: Roles = [...Roles].sort((a, b) => {
		let valueA = a[sortColumn] ?? '';
		let valueB = b[sortColumn] ?? '';

		// Convert to lowercase for case-insensitive sorting
		if (typeof valueA === 'string') valueA = valueA.toLowerCase();
		if (typeof valueB === 'string') valueB = valueB.toLowerCase();

		if (valueA < valueB) return sortAscending ? -1 : 1;
		if (valueA > valueB) return sortAscending ? 1 : -1;
		return 0;
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		
		<div class="ActionBox">

			<div class="title-container">
				<h3 class="title is-2">List of Roles</h3>
				<button class="button is-primary" on:click={addRole}>Add Role</button>
			</div>
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
						 <th on:click={() => toggleSort('Role')} style="cursor: pointer;">Role</th>
					</tr>
				</thead>
				<tbody>
					{#each Roles as role (role.RoleId)}
						<tr on:click={() => location.href=`/Role?RoleId=${role.RoleId}`}>
							<td>{role.Role}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			
		</div>
	</div>
{/if}
