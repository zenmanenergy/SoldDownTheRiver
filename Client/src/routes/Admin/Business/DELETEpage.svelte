<!-- src/routes/Businesses/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetBusiness } from './handleGetBusiness.js';
	import { handleGetBusinessHumans } from './handleGetBusinessHumans.js';
	import { handleGetHumans } from './handleGetHumans.js';
	import { handleSaveBusinessHuman } from './handleSaveBusinessHuman.js';
	import { handleDeleteBusinessHuman } from './handleDeleteBusinessHuman.js';
	import { handleGetLocations } from './handleGetLocations.js';
	
	import { handleGetRoles } from './handleGetRoles.js';
	
	import {Session} from "../../Session.js";
	
	let Svelecte;
	let LocationId=""
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
	let Locations=[]
	let Business = {};
	
	async function setBusiness(data) {
		Business=data
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
	async function setLocations(data) {
		console.log(data)
		Locations=data;
	}
	$: {
		formValid = BusinessName;
	}
	
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		BusinessId = urlParams.get("BusinessId") || "";
		
		const module = await import('svelecte');
		Svelecte = module.default || module;


		await Promise.all([
			handleGetBusiness(Session.SessionId,BusinessId, setBusiness),
			handleGetBusinessHumans(Session.SessionId,BusinessId, setBusinessHumans),
			handleGetHumans(Session.SessionId, setHumans),
			handleGetRoles(Session.SessionId, setRoles),
			handleGetLocations(Session.SessionId, setLocations)
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
		<a href="/Businesses">Back to Businesses</a>
		<div class="ActionBox">
			<form>
				<h3 class="title is-2">Add a Business</h3>
			
				<input type="hidden" bind:value={Business.BusinessId} />
				<input type="hidden" bind:value={Session.SessionId} />
			
				<div class="field">
					<label class="label" for="BusinessName">Name</label>
					<div class="control">
						<input class="input" type="text" id="BusinessName" placeholder="Enter Business Name" bind:value={Business.BusinessName} required/>
					</div>
				</div>

				<div class="field">
					<label class="label" for="LocationId">Location</label>
					<!-- <div class="control">
						<select class="input" id="LocationId" bind:value={Business.LocationId} required>
							<option value="">Select Location</option>
							{#each Locations as Location}
								<option value={Location.LocationId}>{#if Location.Address}{Location.Address} {/if}{Location.City}</option>
							{/each}
						</select>
					</div> -->

					<div class="control">
						<div class="field" id="svelecteBusiness">
							<svelte:component 
								this={Svelecte} 
								bind:value={Business.LocationId} 
								options={Locations.map(Location => ({
									value: Location.LocationId, 
									label: `${Location.Address} ${Location.City}`
								}))} 
							/>
						</div>
						<br/>
					</div>
				</div>
				
				<div class="field">
					<label class="label" for="BusinessHuman">Human</label>
					<div class="control">
						

						<div class="control">
							<div class="field" id="svelecteHumanId">
								<svelte:component 
									this={Svelecte} 
									bind:value={HumanId} 
									options={Humans.map(Human => ({
										value: Human.HumanId, 
										label: `${Human.FirstName} ${Human.LastName}`
									}))} 
								/>
							</div>
							<br/>
						</div>
					</div>
				</div>
				<div class="field">
					<label class="label" for="BusinessHuman">Role</label>
					<div class="control">
						<div class="control">
							<div class="field" id="svelecteRoleId">
								<svelte:component 
									this={Svelecte} 
									bind:value={RoleId} 
									options={Roles.map(Role => ({
										value: Role.RoleId, 
										label: Role.Role
									}))} 
								/>
							</div>
							<br/>
						</div>

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
							
								<tr >
									<td><a href="/Human?HumanId={human.HumanId}">{human.FirstName}</a></td>
									<td><a href="/Human?HumanId={human.HumanId}">{human.LastName}</a></td>
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
					<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId, Business.BusinessId, Business.BusinessName, Business.LocationId, formValid)}>Save</button>
					{#if BusinessId.length}
						<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, Business.BusinessId)}>Delete</button>
					{/if}
					</div>
				</div>
			</form>
		
		</div>
		{#if LastModified}
		<small>Last Modified: {moment.utc(LastModified).local().fromNow()}</small>
		{/if}
	</div>
{/if}
	