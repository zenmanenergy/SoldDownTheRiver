<style>
	@import '/static/FormPages.css';
</style>

<script>
	import { onMount } from 'svelte';
	import { handleGetRoles } from './handleGetRoles.js';
	import { Session } from "../Session.js";

	export let Roles = [];
	let isLoading = true;

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
			<table class="ClickableTable" width="100%">
				<thead>
					<tr>
						<th>Role</th>
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
