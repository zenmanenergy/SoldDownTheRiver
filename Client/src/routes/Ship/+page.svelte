<!-- src/routes/Ships/+page.svelte -->

	<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetShip } from './handleGetShip.js';
	import { handleGetShipVoyages } from './handleGetShipVoyages.js';
	import { handleGetCaptains } from './handleGetCaptains.js';
	import { handleGetLocations } from '../Locations/handleGetLocations.js';
	import { handleGetTransactions } from './handleGetTransactions.js';
	import { Session } from "../Session.js";
	
	let ShipId = "";
	let BuildDate = null;
	let Notes = "";
	let ShipType = "";
	let Size = "";
	let Ship={ShipId:"", ShipName:"", BuildDate:null, Notes:"", ShipType:"", Size:"", HomePortLocationId:"",AgentHumanId:""};
	let Captains = [];
	let Voyages = [];
	let Locations = [];
	let Transactions=[]
	let Svelecte;
	let HomePortLocationId;
	let AgentHumanId;
	let Query=""
	
	let formValid = false;
	let isLoading = true;
	
	async function setShip(data) {
		Ship.ShipId = data.ShipId || "";
		Ship.ShipName = data.ShipName || "";
		if (data.BuildDate){
			Ship.BuildDate = moment(data.BuildDate).format("YYYY-MM-DD")||"";
			
		}
		Ship.Notes = data.Notes || "";
		Ship.ShipType = data.ShipType || "";
		Ship.Size = data.Size || "";
		Ship.HomePortLocationId = data.HomePortLocationId || "";
		Ship.AgentHumanId = data.AgentHumanId || "";
		
		console.log("Ship", Ship)
		// console.log("Ship.ShipId.length", Ship.ShipId.length)
	}
	async function setCaptains(data) {
		Captains = [{HumanId: "add_new", FirstName: "[Add New]", LastName: ""}, ...data];
	}

	async function setLocations(data) {
		// Locations = [{HumanId: "add_new", City: "[Add New]", State: ""}, ...data];
		Locations=data
	}
	async function setVoyages(data){
		Voyages=data;
	}
	async function setTransactions(data) {
		Transactions=data
	}
	$: {
		formValid = Ship.ShipName;
	}
	
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		ShipId = urlParams.get("ShipId") || "";
		await Promise.all([
			handleGetShip(Session.SessionId, ShipId, setShip),
			handleGetShipVoyages(Session.SessionId, ShipId, setVoyages),
			handleGetLocations(Session.SessionId,setLocations),
			handleGetCaptains(Session.SessionId,Query, setCaptains),
			handleGetTransactions(Session.SessionId,ShipId, setTransactions)
		]);
		const module = await import('svelecte');
		Svelecte = module.default || module;
		
		Promise.resolve().then(() => {
			const svelecteLocation = document.querySelector('#svelecteLocation');
			const svelecteLocationSearch = svelecteLocation.querySelector('input');
			if (svelecteLocationSearch) {
				svelecteLocationSearch.addEventListener('input', handleLocationInput);
			}

		});

		
	
		isLoading = false;
	});
	$: if (HomePortLocationId) {
		console.log("HomePortLocationId changed:", HomePortLocationId);
	}
	function handleLocationInput(event) {
		
		if (Ship.HomePortLocationId === "add_new") {
			// Redirect to the desired page
			window.location.href = "/path_to_new_page"; // replace "path_to_new_page" with your desired path
			return;
		}
		if (event.target.value.length<=1){
			Query=event.target.value
			handleGetCaptains(Session.SessionId, Query, setCaptains)
		}
	}
	function handleLocationSelection(event) {
		if (Ship.HomePortLocationId === "add_new") {
			// Redirect to the desired page
			window.location.href = "/path_to_new_page"; // replace "path_to_new_page" with your desired path
			return;
		}
		// existing handleLocationInput logic
		handleLocationInput(event);
	}
	
	function addVoyage(){
		location.href="/Voyage?VoyageId=&ShipId="+Ship.ShipId
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
					<h3 class="title is-2">Add/Edit a Ship</h3>
					{#if Ship.ShipId.length}
					<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, Ship.ShipId)}>Delete</button>
					{/if}
				</div>
				<input type="hidden" bind:value={Ship.ShipId} />
		
				<div class="field">
					<label class="label" for="ShipName">Ship Name</label>
					<div class="control">
						<input class="input" type="text" id="ShipName" placeholder="Enter ShipName" bind:value={Ship.ShipName} required />
					</div>
				</div>

				<div class="field">
					<label class="label" for="BuildDate">Build Date</label>
					<div class="control">
						<input class="input" type="date" id="BuildDate" placeholder="Enter Build Date" bind:value={Ship.BuildDate} />
					</div>
				</div>
		
				<div class="field">
					<label class="label" for="Notes">Notes</label>
					<div class="control">
						<input class="input" type="text" id="Notes" placeholder="Enter Notes" bind:value={Ship.Notes} />
					</div>
				</div>
		
				<div class="field">
					<label class="label" for="ShipType">Ship Type</label>
					<div class="control">
						<input class="input" type="text" id="ShipType" placeholder="Enter Ship Type" bind:value={Ship.ShipType} />
					</div>
				</div>
		
				<div class="field">
					<label class="label" for="Size">Size</label>
					<div class="control">
						<input class="input" type="text" id="Size" placeholder="Enter Size" bind:value={Ship.Size} />
					</div>
				</div>
		
				<div class="field">
					<label class="label" for="Size">Home Port Location <a class="AddLink" href="/Location?LocationId=">Add Location</a></label>
					<div class="control">
						

							<svelte:component 
								this={Svelecte} 
								bind:value={Ship.HomePortLocationId} 
								on:input={handleLocationSelection} 
								options={Locations.map(location => ({
									value: location.LocationId, 
									label: `${location.Address}`
								}))} 
							/>
						</div>
						
					</div>
		
				
				<div class="field">
					<div class="control">
						<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId, Ship, formValid)}>Save</button>
						
					</div>
				</div>
			</form>

			
			<br/>
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-2">Voyages</h3>
					<button class="button is-primary" type="button" on:click={addVoyage}>Add Voyage</button>
				</div>
				<form>
				
				<table class="ClickableTable" width=100%>
					<thead>
						<tr>
							<th>From</th>
							<th>To</th>
						</tr>
					</thead>
					<tbody>
						{#each Voyages as Voyage}
							<tr on:click={() => window.location.href = `/Voyage?VoyageId=${Voyage.VoyageId}`}>
								<td>{Voyage.StartCity} {Voyage.StartState} {moment(Voyage.StartDate).format('MMMM D, YYYY')}</td>
								<td>{Voyage.EndCity} {Voyage.EndState} {moment(Voyage.EndDate).format('MMMM D, YYYY')}</td>
							</tr>
						{/each}

						
					</tbody>
				</table>
				
			</div>
		</div>
	</div>
	{/if}
