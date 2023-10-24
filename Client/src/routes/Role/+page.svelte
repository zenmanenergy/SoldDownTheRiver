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
	import { handleGetRoleHumans } from './handleGetRoleHumans.js';
	import {Session} from "../Session.js";

	
	let formValid = false;
	let isLoading = true;
	let Role={RoleId :"", Role : "", LastModified : ""}
	let RoleHumans=[]
	let HumanId=""
	let Humans=[]
	let Query="a"
	
	async function setRole(data) {
		Role.RoleId = data.RoleId || "";
		Role.Role = data.Role || "";
		Role.LastModified = data.LastModified || "";
		
	}
	async function setRoleHumans(data) {
		RoleHumans=data
	}
	async function setHumans(data) {
		Humans=data
	}
	
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		Role.RoleId = urlParams.get("RoleId") || "";
		await Promise.all([
			await handleGetRole(Session.SessionId,Role.RoleId,setRole),
			await handleGetRoleHumans(Session.SessionId,Role.RoleId,setRoleHumans)
		]);
		
		isLoading = false;
	});
	
	async function confirmDelete() {
		const userConfirmed = confirm('Are you sure you want to delete this role?\n\nWarning!!! it will delete all associations with the human records too');
		if (userConfirmed) {
			console.log("delete")
			await handleDelete(Session.SessionId, Role.RoleId);
		}
	}
	function addExistingHuman(){
		window.location.href = '/Role/NewOrOld?RoleId='+Role.RoleId+'&Role='+Role.Role;
	}
	function addNewHuman(){
		window.location.href = '/Human/'+Role.RoleId;
	}
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
				
				<div class="title-container">
					<h3 class="title is-2">Add/Edit a Role</h3>
					{#if Role.RoleId.length}
						<button class="button is-danger" type="button" on:click={confirmDelete}>Delete</button>
					{/if}
				</div>
				<div class="control">
					
					<div class="field">
						<label class="label" for="RoleId">RoleId</label>
							
						<input
							class="input"
							type="text"
							id="RoleId"
							placeholder="Enter Role Id"
							bind:value={Role.RoleId}
							required
						/>
						</div>
					</div>
					<br/>
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
						<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId,Role, formValid)}>Save</button>
						
					</div>
				</div>
			</form>
			{#if Role.LastModified}
				<small>Last Modified: {moment.utc(Role.LastModified).local().fromNow()}</small>
			{/if}

			<br/>
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-2">List of Humans</h3>
					<button class="button is-danger" type="button" on:click={addExistingHuman}>Add Existing</button>
					<button class="button is-danger" type="button" on:click={addNewHuman}>Add New</button>
				</div>
				<form>
				<div class="field">
					<div class="control">
						<!-- <input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" /> -->
					</div>
				
					</div>
				</form>
				<table class="ClickableTable" width=100%>
					<thead>
						<tr>
							<th>First Name</th>
							<th>Last Name</th>
							<th>Last Modified</th>
						</tr>
					</thead>
					<tbody>
						{#each RoleHumans as human}
							<tr on:click={() => location.href=`/Human/${human.RoleId}?HumanId=${human.HumanId}`}>
								<td>{human.FirstName}</td>
								<td>{human.LastName}</td>
								<td>{moment.utc(human.LastModified).local().fromNow()}</td>
							</tr>
						{/each}
						
					</tbody>
				</table>
				
			</div>
		</div>
	</div>
{/if}
