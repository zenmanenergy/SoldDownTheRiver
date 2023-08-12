<!-- src/routes/Roles/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetRole } from './handleGetRole.js';
	import {Session} from "../Session.js";

	
	let formValid = false;
	let isLoading = true;
	let Role={RoleId :"", Role : "", LastModified : ""}
	$: {
		formValid = Role.Role;
	}
	async function setRole(data) {
		Role.RoleId = data.RoleId || "";
		Role.Role = data.Role || "";
		Role.LastModified = data.LastModified || "";
		
	}
		
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		Role.RoleId = urlParams.get("RoleId") || "";
		await Promise.all([
			await handleGetRole(Session.SessionId,Role.RoleId,setRole)
			
		]);
		
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
							bind:value={Role.RoleId} />
						<input
							class="input"
							type="text"
							id="Role"
							placeholder="Enter Role Name"
							bind:value={Role.Role}
							required
						/>
					</div>
				</div>

				<div class="field">
					<div class="control">
						<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId,Role, formValid)}>Save</button>
						{#if Role.RoleId.length}
							<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId,Role.RoleId)}>Delete</button>
						{/if}
					</div>
				</div>
			</form>
			{#if Role.LastModified}
				<small>Last Modified: {moment.utc(Role.LastModified).local().fromNow()}</small>
			{/if}
		</div>
	</div>
{/if}
