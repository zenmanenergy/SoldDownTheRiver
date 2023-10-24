<!-- src/routes/Voyages/+page.svelte -->
<style>
		@import '/static/FormPages.css';
	</style>
	<script>
		import moment from 'moment';
		import { onMount } from 'svelte';
		import { handleSave } from './handleSave.js';
		import { handleDelete } from './handleDelete.js';
		import { handleGetVoyage } from './handleGetVoyage.js';
		import { handleGetCaptains } from './handleGetCaptains.js';
		import { handleGetShips } from './handleGetShips.js';
		import { handleGetHumans } from './handleGetHumans.js';
		import { handleSaveVoyageHuman } from './handleSaveVoyageHuman.js';
		import { handleGetVoyageHumans } from './handleGetVoyageHumans.js';
		import { handleDeleteVoyageHuman } from './handleDeleteVoyageHuman.js';
		import { handleGetRoles } from './handleGetRoles.js';
		import { Session } from '../Session.js';
		import {handleGetLocations} from './handleGetLocations.js';

		let Svelecte;
		let VoyageId = '';
		let ShipId = '';
		let StartLocationId = '';
		let EndLocationId = '';
		let StartDate = null;
		let EndDate = null;
		let Notes = '';
		let VoyageHumanId="";
		let VoyageHumanRoleId="";
		let VoyageHumanNotes="";
		let Voyage={VoyageId:"", ShipId:ShipId, StartLocationId:"", EndLocationId:"", StartDate:null, EndDate:null, Notes:""};
		let Ships=[]
		let Humans = [];
		let VoyageHumans=[];
		let Roles = [];
		let Locations = [];
		let Captains = [];
		let Query=""
	
		let formValid = false;
		let isLoading = true;
	
		async function setLocations(data) {
			Locations=data
		}
		async function setCaptains(data){
			Captains=data
		}
		async function setVoyage(data) {

			if (data.VoyageId){

				Voyage.VoyageId = data.VoyageId || "";
				Voyage.ShipId = data.ShipId || "";
				Voyage.StartLocationId = data.StartLocationId || "";
				Voyage.CaptainHumanId=data.CaptainHumanId
				Voyage.EndLocationId = data.EndLocationId || "";
				if (data.StartDate){
					Voyage.StartDate = moment(data.StartDate).format("YYYY-MM-DD")||"";
				}
				if (data.EndDate){
					Voyage.EndDate = moment(data.EndDate).format("YYYY-MM-DD")||"";
				}
				Voyage.Notes = data.Notes || "";
			}
		}
		async function setShips(data) {
			Ships = data;
		}
		async function setHumans(data) {
			Humans = data;
		}
		async function setVoyageHumans(data) {
			VoyageHumans = data;
		}
		async function setRoles(data) {
			Roles = data;
		}
		
		$: {
			formValid = Voyage.ShipId;
		}
	
		onMount(async () => {
			
			await Session.handleSession();
			const urlParams = new URLSearchParams(window.location.search);
			VoyageId = urlParams.get('VoyageId') || '';
			ShipId = urlParams.get('ShipId') || '';
			Voyage.ShipId=ShipId
			console.log(Voyage)
			
			await Promise.all([
				handleGetVoyage(Session.SessionId, VoyageId, setVoyage),
				handleGetShips(Session.SessionId, setShips),
				handleGetVoyageHumans(Session.SessionId,VoyageId,setVoyageHumans),
				handleGetLocations(Session.SessionId,setLocations),
				handleGetCaptains(Session.SessionId,setCaptains)

			]);
			const module = await import('svelecte');
			Svelecte = module.default || module;

			
			isLoading = false;
		});

		
		
	</script>
	
	{#if isLoading}
		<div class="loading-screen">
			<div class="spinner"></div>
		</div>
	{:else}
		<div class="section">
			<a href="/Voyages?">Back to Voyages</a>
			<div class="ActionBox">
				<form>
					<h3 class="title is-2">Add a Voyage</h3>
					<input type="hidden" bind:value={Voyage.VoyageId} />
	

					<div class="field">
						<label class="label" for="Size">Ship</label>
						<div class="control">
							<div id="svelecteStartLocation">
								<Svelecte bind:value={Voyage.ShipId} options={Ships.map(Ship => ({value: Ship.ShipId, label: Ship.ShipName}))} />
							</div>
						</div>
					</div>
					<div class="field">
						<label class="label" for="Size">Ship Captain</label>
						<div class="control">
							<div id="svelecteEndLocation">
								<Svelecte bind:value={Voyage.CaptainHumanId} options={Captains.map(Captain => ({value: Captain.HumanId, label: Captain.FirstName+" "+Captain.LastName}))} />
								
							</div>
	
						</div>
					</div>
					<div class="field">
						<label class="label" for="Size">Start Location</label>
						<div class="control">
							<div id="svelecteStartLocation">
								<Svelecte bind:value={Voyage.StartLocationId} options={Locations.map(location => ({value: location.LocationId, label: location.City+" "+location.State}))} />
							</div>
						</div>
					</div>
					<div class="field">
						<label class="label" for="StartDate">Start Date</label>
						<div class="control">
							<input class="input" type="date" id="StartDate" bind:value={Voyage.StartDate} />
						</div>
					</div>
	
					
					<div class="field">
						<label class="label" for="Size">End Location</label>
						<div class="control">
							<div id="svelecteEndLocation">
								<Svelecte bind:value={Voyage.EndLocationId} options={Locations.map(location => ({value: location.LocationId, label: location.City+" "+location.State}))} />
								
							</div>
	
						</div>
					</div>
	
					<div class="field">
						<label class="label" for="EndDate">End Date</label>
						<div class="control">
							<input class="input" type="date" id="EndDate" bind:value={Voyage.EndDate} />
						</div>
					</div>
					<div class="field">
						<label class="label" for="Notes">Notes</label>
						<div class="control">
							<input class="input" type="text" id="Notes" placeholder="Enter Notes" bind:value={Voyage.Notes}/>
						</div>
					</div>
					
					
						
					<div class="field">
						<div class="control">
							<button class="button is-primary" type="button" on:click={() =>   handleSave(Session.SessionId,Voyage,formValid   ) }> Save</button>
							{#if VoyageId.length}
								<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, VoyageId)}>Delete</button>
							{/if}
						</div>
					</div>

					<div class="ActionBox">
						<h3 class="title is-2">List of Enslaved People</h3>
						<table class="ClickableTable" width=100%>
							<thead>
							<tr>
								<th>First Name</th>
								<th>Last Name</th>
								<th>Role</th>
							</tr>
							</thead>
							<tbody>
							{#each VoyageHumans as Human}
								<tr on:click={() => window.location.href = `/Voyage/${Human.RoleId}?VoyageId=${VoyageId}&HumanId=${Human.HumanId}`}>
									<td>{Human.FirstName}</td>
									<td>{Human.LastName}</td>
									<td>{Human.Role}</td>
								</tr>
							{/each}
							</tbody>
						</table>
						</div>
				</form>
			</div>
		</div>
	{/if}
	