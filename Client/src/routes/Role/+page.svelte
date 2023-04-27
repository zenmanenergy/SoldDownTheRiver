<!-- src/routes/Roles/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';
	import {Session} from "../Session.js";

	let RoleId = "";
	let Role = "";
	let formValid = false;
	let isLoading = true;

	$: {
		formValid = Role;
	}
	async function setRole(_RoleId,_Role) {
		if (_RoleId){
			RoleId = _RoleId;
			Role = _Role;
		}
		
	}
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		RoleId = urlParams.get("RoleId") || "";
		handleGet(Session.SessionId,RoleId, setRole);
		
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
						<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId,RoleId,Role, formValid)}>Save</button>
						{#if Role.length}
							<button class="button is-danger" type="button" on:click={() => handleDelete(Session.WSessionId,RoleId,Role)}>Delete</button>
						{/if}
					</div>
				</div>
			</form>
			<small>Last Modified: {moment(LastModified).fromNow()}</small>
		</div>
	</div>
{/if}
