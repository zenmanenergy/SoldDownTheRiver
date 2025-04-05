<!-- src/routes/Roles/+page.svelte -->


<script>
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { Session } from "../Session.js";
	import {handleGetRole } from './handleGetRole.js'

	let formValid = false;
	let isLoading = true;
	let Role = { RoleId: "", Role: "", LastModified: "" };

	async function setRole(data) {
		Role.RoleId = data.RoleId || "";
		Role.Role = data.Role || "";
		Role.LastModified = data.LastModified || "";
	}

	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		Role.RoleId = urlParams.get("RoleId") || "";
		await handleGetRole(Session.SessionId, Role.RoleId, setRole);
		isLoading = false;
	});

	async function confirmDelete() {
		const userConfirmed = confirm('Are you sure you want to delete this role?\n\nWarning!!! It will delete all associations with human records too.');
		if (userConfirmed) {
			await handleDelete(Session.SessionId, Role.RoleId);
		}
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<div class="ActionBox">
			<form>
				<div class="title-container">
					<h3 class="title is-2">Add/Edit a Role</h3>
					{#if Role.RoleId.length}
						<button class="button is-danger" type="button" on:click={confirmDelete}>Delete</button>
					{/if}
				</div>
				
				<!-- RoleId is now read-only -->
				<div class="control">
					<div class="field">
						<label class="label" for="RoleId">Role ID</label>
						<input
							class="input"
							type="text"
							id="RoleId"
							bind:value={Role.RoleId}
							readonly
						/>
					</div>
				</div>

				<br />

				<!-- Editable Role Name -->
				<div class="control">
					<label class="label" for="Role">Name</label>
					<div class="field">
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
						<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId, Role, formValid)}>Save</button>
					</div>
				</div>
			</form>

		</div>
	</div>
{/if}
