<!-- src/routes/Voyages/+page.svelte -->

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetVoyage } from './handleGetVoyage.js';
	import { handleGetCaptains } from './handleGetCaptains.js';
	import { handleGetShips } from './handleGetShips.js';
	// import { handleGetHumans } from './handleGetHumans.js';
	import { handleSaveVoyageHuman } from './handleSaveVoyageHuman.js';
	import { handleGetVoyageHumans } from './handleGetVoyageHumans.js';
	// import { handleDeleteVoyageHuman } from './handleDeleteVoyageHuman.js';
	// import { handleGetRoles } from './handleGetRoles.js';
	import { Session } from '../Session.js';
	import {handleGetLocations} from './handleGetLocations.js';
	import { handleGetSellers } from './handleGetSellers.js';
	import { handleGetBuyers } from './handleGetBuyers.js';
	import { handleGetShippingAgents } from './handleGetShippingAgents.js';
	import { handleGetCollectorAgents } from './handleGetCollectorAgents.js';

	let Svelecte;
	let VoyageId = '';
	let ShipId = '';
	// let StartLocationId = '';
	// let EndLocationId = '';
	// let StartDate = null;
	// let EndDate = null;
	// let Notes = '';
	// let VoyageHumanId="";
	// let VoyageHumanRoleId="";
	// let VoyageHumanNotes="";
	let Voyage={VoyageId:"", ShipId:ShipId, StartLocationId:"", EndLocationId:"", StartDate:null, EndDate:null, Notes:""};
	let Ships=[]
	let Humans = [];
	let VoyageHumans=[];
	let Roles = [];
	let Locations = [];
	let Captains = [];
	let Sellers = [];
	let Buyers = [];
	let ShippingAgents = [];
	let CollectorAgents = [];
	// let Query=""
	
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
	async function setSellers(data) {
		Sellers = data;
	}
	async function setBuyers(data) {
		Buyers = data;
	}
	async function setShippingAgents(data) {
		ShippingAgents = data;
	}
	async function setCollectorAgents(data) {
		CollectorAgents = data;
	}
	async function setSaveVoyageHuman(data) {
		console.log("saved",data)
	}
	$: {
		formValid = Voyage.ShipId;
	}

	// Utility function to get a URL parameter by name
	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	onMount(async () => {
		await Session.handleSession();
		VoyageId = getURLVariable('VoyageId') || '';
		ShipId = getURLVariable('ShipId') || '';
		Voyage.ShipId = ShipId;
		console.log(Voyage);
		
		await Promise.all([
			handleGetVoyage(Session.SessionId, VoyageId, setVoyage),
			handleGetShips(Session.SessionId, setShips),
			handleGetVoyageHumans(Session.SessionId,VoyageId,setVoyageHumans),
			handleGetLocations(Session.SessionId,setLocations),
			handleGetCaptains(Session.SessionId,setCaptains),
			handleGetSellers(Session.SessionId, setSellers),
			handleGetBuyers(Session.SessionId, setBuyers),
			handleGetShippingAgents(Session.SessionId, setShippingAgents),
			handleGetCollectorAgents(Session.SessionId, setCollectorAgents)
		]);
		const module = await import('svelecte');
		Svelecte = module.default || module;

		
		isLoading = false;
	});

	function addEnslavedPerson() {
		window.location.href = '/Voyage/EnslavedPerson?VoyageId='+VoyageId+'&HumanId=';
	}

	
	
</script>

<style>
	.truncated-select {
		width: 150px; /* Set a fixed width */
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<div class="ActionBox">


			<form>
				<div class="title-container">
					<h3 class="title is-2">Voyage</h3>
					{#if VoyageId.length}
						<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, VoyageId)}>Delete</button>
					{/if}
				</div>
				<input type="hidden" bind:value={Voyage.VoyageId} />
				<div class="field">
					<label class="label" for="Size">Ship</label>
					<div class="control">
						<div id="svelecteStartLocation">
							<svelte:component 
								this={Svelecte} 
								bind:value={Voyage.ShipId} 
								options={Ships.map(Ship => ({
									value: Ship.ShipId, 
									label: Ship.ShipName
								}))} 
							/>
						</div>
					</div>
				</div>
				<div class="field">
					<label class="label" for="Size">Ship Captain <a class="AddLink" href="/Human?returnPath=/Voyage?VoyageId={Voyage.VoyageId}">Add Captain</a></label>
					<div class="control">
						<div id="svelecteEndLocation">
							<svelte:component 
								this={Svelecte} 
								bind:value={Voyage.CaptainHumanId} 
								options={Captains.map(Captain => ({
									value: Captain.HumanId, 
									label: `${Captain.FirstName || ''} ${Captain.LastName || ''}`
								}))} 
							/>
						</div>

					</div>
				</div>
				<div class="field">
					<label class="label" for="Size">Start Location <a class="AddLink" href="/Location?LocationId=">Add Location</a></label>
					<div class="control">
						<div id="svelecteStartLocation">
							<svelte:component 
								this={Svelecte} 
								bind:value={Voyage.StartLocationId} 
								options={Locations.map(location => ({
									value: location.LocationId, 
									label: `${location.Address}`
								}))} 
							/>
						</div>
					</div>
				</div>
				
				
				<div class="field">
					<label class="label" for="Size">End Location <a class="AddLink" href="/Location?LocationId=">Add Location</a></label>
					<div class="control">
						<div id="svelecteEndLocation">
							<svelte:component 
								this={Svelecte} 
								bind:value={Voyage.EndLocationId} 
								options={Locations.map(location => ({
									value: location.LocationId, 
									label: `${location.Address}`
								}))} 
							/>

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
						
					</div>
				</div>

				{#if VoyageId}
					<div class="ActionBox" style="disabled:true">
						<!-- Enslaved People Table -->
						<div class="title-container">
							<h3 class="title is-2">List of Enslaved People</h3>
							<button class="button is-primary" on:click={addEnslavedPerson}>Add Enslaved Person</button>
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>Name</th>
									<th>Seller</th>
									<th>Shipping Agent</th>
									<th>Buyer</th>
									<th>Collector</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Enslaved') as Human}
									<tr on:click={() => window.location.href = `/Human?HumanId=${Human.HumanId}`} style="cursor:pointer;">
										<td>{Human.FirstName || ''} {Human.LastName || ''}</td>
										<td>
											<select class="truncated-select" bind:value={Human.owner_humanid} on:change={() => handleSaveVoyageHuman(Voyage.VoyageId,Human, setSaveVoyageHuman)}>
												<option></option>
												{#each Sellers as Seller}
												
													<option value={Seller.HumanId}>
														{Seller.FirstName || ''} {Seller.LastName || ''}
													</option>
												{/each}
											</select>
										</td>
										<td>
											<select class="truncated-select" bind:value={Human.shippingagent_humanid} on:change={() => handleSaveVoyageHuman(Voyage.VoyageId,Human, setSaveVoyageHuman)}>
												<option></option>
												{#each ShippingAgents as ShippingAgent}
													<option value={ShippingAgent.HumanId}>
														{ShippingAgent.FirstName || ''} {ShippingAgent.LastName || ''}
													</option>
												{/each}
											</select>
										</td>
										<td>
											<select class="truncated-select" bind:value={Human.owner2_humanid} on:change={() => handleSaveVoyageHuman(Voyage.VoyageId,Human, setSaveVoyageHuman)}>
												<option></option>
												{#each Buyers as Buyer}
													<option value={Buyer.HumanId}>
														{Buyer.FirstName || ''} {Buyer.LastName || ''}
													</option>
												{/each}
											</select>
										</td>
										<td>
											<select class="truncated-select" bind:value={Human.collectoragent_humanid} on:change={() => handleSaveVoyageHuman(Voyage.VoyageId,Human, setSaveVoyageHuman)}>
												<option></option>
												{#each CollectorAgents as CollectorAgent}
													<option value={CollectorAgent.HumanId}>
														{CollectorAgent.FirstName || ''} {CollectorAgent.LastName || ''}
													</option>
												{/each}
											</select>
										</td>
										<td>
											<textarea bind:value={Human.Notes} on:change={() => handleSaveVoyageHuman(Voyage.VoyageId,Human, setSaveVoyageHuman)}></textarea>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>

						<!-- Captain Table -->
						<div class="title-container">
							<h3 class="title is-2">Captain</h3>
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>First Name</th>
									<th>Last Name</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Captain') as Human}
									<tr on:click={() => window.location.href = `/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>

						<!-- Owner 1 Table -->
						<div class="title-container">
							<h3 class="title is-2">Owner 1</h3>
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>First Name</th>
									<th>Last Name</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Owner 1') as Human}
									<tr on:click={() => window.location.href = `/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>

						<!-- Owner 2 Table -->
						<div class="title-container">
							<h3 class="title is-2">Owner 2</h3>
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>First Name</th>
									<th>Last Name</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Owner 2') as Human}
									<tr on:click={() => window.location.href = `/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>

						<!-- Shipping Agent Table -->
						<div class="title-container">
							<h3 class="title is-2">Shipping Agent</h3>
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>First Name</th>
									<th>Last Name</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Shipping Agent') as Human}
									<tr on:click={() => window.location.href = `/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>

						<!-- Collector Agent Table -->
						<div class="title-container">
							<h3 class="title is-2">Collector Agent</h3>
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>First Name</th>
									<th>Last Name</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Collector Agent') as Human}
									<tr on:click={() => window.location.href = `/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/if}
			</form>
		</div>
	</div>
{/if}
