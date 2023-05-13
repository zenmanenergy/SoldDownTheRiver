<!-- src/routes/Businesses/+page.svelte -->
<style>
	@import '/static/FormPages.css';
  </style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';
	import { handleGetBusinessHumans } from './handleGetBusinessHumans.js';
	import { handleGetHumans } from './handleGetHumans.js';
	import { handleSaveBusinessHuman } from './handleSaveBusinessHuman.js';
	import { handleDeleteBusinessHuman } from './handleDeleteBusinessHuman.js';
	
	import { handleGetRoles } from './handleGetRoles.js';
	
	import {Session} from "../Session.js";
  
	let RoleId=""
	let HumanId=""
	let BusinessId="";
	let BusinessName = "";
	let LastModified = "";
	let formValid = false;
	let isLoading = true;
	let BusinessHumans=[]
	let Humans=[]
	let Roles=[]
  
	async function setName(newBusinessName, newLastModified) {
	  BusinessName = newBusinessName;
	  LastModified = newLastModified;
	}
	async function setBusinessHumans(data) {
	  BusinessHumans=data;
	}
	async function setHumans(data) {
	  Humans=data;
	}
	async function setRoles(data) {
		Roles=data;
	}
	$: {
	  formValid = BusinessName;
	}
  
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		BusinessId = urlParams.get("BusinessId") || "";
		
		if (BusinessId){
			await Promise.all([
				handleGet(Session.SessionId,BusinessId, setName),
				handleGetBusinessHumans(Session.SessionId,BusinessId, setBusinessHumans),
				handleGetHumans(Session.SessionId, setHumans),
				handleGetRoles(Session.SessionId, setRoles)
			]);
		
		}
		console.log("BusinessId", BusinessId)
		isLoading = false;
	});
  </script>
  
  
  
  {#if isLoading}
	<div class="loading-screen">
	  <div class="spinner"></div>
	</div>
  {:else}
  
	<div class="section">
		<a href="/Businesses">Back to Businesses</a>
		<div class="ActionBox">
	  <form>
		<h3 class="title is-2">Add a Business</h3>
  
		<input type="hidden" bind:value={BusinessId} />
		<input type="hidden" bind:value={Session.SessionId} />
  
		<div class="field">
		  <label class="label" for="BusinessName">Name</label>
		  <div class="control">
			<input class="input" type="text" id="BusinessName" placeholder="Enter Business Name" bind:value={BusinessName} required/>
		  </div>
		</div>
		<div class="field">
			<label class="label" for="BusinessHuman">Human</label>
			<div class="control">
				<select class="input" id="HumanId" bind:value={HumanId} required>
					<option value="">Select Human</option>
					{#each Humans as Human}
						<option value={Human.HumanId}>{Human.FirstName} {Human.LastName}</option>
					{/each}
				</select>
				<select class="input" id="RoleId" bind:value={RoleId} required>
					<option value="">Select Role</option>
					{#each Roles as Role}
						<option value={Role.RoleId}>{Role.Role}</option>
					{/each}
				</select>
				<button class="button" type="button"on:click={() => handleSaveBusinessHuman(Session.SessionId,BusinessId,HumanId, RoleId)} >Add to Business</button>
			</div>
		</div>
		<div class="ActionBox">
			<h3 class="title is-2">List of Humans</h3>
			<table width=100%>
			  <thead>
				<tr>
				  <th>First Name</th>
				  <th>Last Name</th>
				  <th>Role</th>
				  <th>Last Modified</th>
				  <th>Delete</th>
				</tr>
			  </thead>
			  <tbody>
				{#each BusinessHumans as human}
				  <tr>
					<td>{human.FirstName}</td>
					<td>{human.LastName}</td>
					<td>{human.Role}</td>
					<td>{moment.utc(human.LastModified).local().fromNow()}</td>
					<td><button style="padding:0px;padding-left:5px;padding-right:5px;" on:click={() => handleDeleteBusinessHuman(Session.SessionId,BusinessId, human.HumanId)}>X</button></td>
        
				  </tr>
				{/each}
			  </tbody>
			</table>
		  </div>


		<div class="field">
		  <div class="control">
			<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId, BusinessId, BusinessName,formValid)}>Save</button>
			{#if BusinessId.length}
			  <button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, BusinessId)}>Delete</button>
			{/if}
		  </div>
		</div>
	  </form>
	  {#if LastModified}
		<small>Last Modified: {moment.utc(LastModified).local().fromNow()}</small>
	  {/if}
	</div>
	</div>
  {/if}
  