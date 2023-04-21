<!-- src/routes/Roles/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>

<script>
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';

	let RoleId = "";
	let Role = "";
	let formValid = false;
	let isLoading = true;

	$: {
		formValid = Role;
	}
	async function setRole(_RoleId,_Role) {
		console.log(RoleId,Role)
		RoleId = _RoleId;
		Role = _Role;
	}
	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		RoleId = urlParams.get("RoleId") || "";
		if (RoleId) {
			handleGet(RoleId, setRole);
		}
		console.log("RoleId", RoleId);
		isLoading = false;
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/Roles">Back to Roles</a>
		<div class="ActionBox">
			<form>
				<h3 class="title is-2">Add a Role</h3>

				<div class="field">
					<label class="label" for="Role">Name</label>
					<div class="control">
						<input type="hidden" 
							id="RoleId" 
							bind:value={RoleId} />
						<input
							class="input"
							type="text"
							id="Role"
							placeholder="Enter Role Name"
							bind:value={Role}
							required
						/>
					</div>
				</div>

				<div class="field">
					<div class="control">
						<button class="button is-primary" type="button" on:click={() => handleSave(RoleId,Role, formValid)}>Save</button>
						{#if Role.length}
							<button class="button is-danger" type="button" on:click={() => handleDelete(RoleId,Role)}>Delete</button>
						{/if}
					</div>
				</div>
			</form>
		</div>
	</div>
{/if}
