<!-- src/routes/Voyages/+page.svelte -->

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetVoyage } from './handleGetVoyage.js';
	import { handleGetShips } from './handleGetShips.js';
	// import { handleGetHumans } from './handleGetHumans.js';
	import { handleSaveVoyageHuman } from './handleSaveVoyageHuman.js';
	import { handleGetVoyageHumans } from './handleGetVoyageHumans.js';
	import { handleDeleteVoyageHuman } from './handleDeleteVoyageHuman.js';
	// import { handleGetRoles } from './handleGetRoles.js';
	import {Session} from '../../Session.js';
	import {handleGetLocations} from './handleGetLocations.js';
	import { handleSaveReferenceLink } from '../Reference/handleSaveReferenceLink.js';
	import { handleGetLinkReferences } from '../References/handleGetLinkReferences.js';
	import { handleSearchHumans } from '../Humans/handleSearchHumans.js';

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
	let voyageReferences = [];

	// Variables for available humans search functionality
	let searchQuery = '';
	let availableHumans = [];
	let sortColumnSearch = '';
	let sortDirectionSearch = 1;
	let searchTimeout;
	let selectedRoleForHuman = {}; // map human.HumanId --> selected role

	// Define voyage-specific roles
	const voyageRoles = [
		{ id: 'Enslaved', name: 'Enslaved' },
		{ id: 'Captain', name: 'Captain' },
		{ id: 'Owner 1', name: 'Owner 1' },
		{ id: 'Owner 2', name: 'Owner 2' },
		{ id: 'Shipping Agent', name: 'Shipping Agent' },
		{ id: 'Collector Agent', name: 'Collector Agent' }
	];

	let formValid = false;
	let isLoading = true;
	let isReferencesLoading = true;
	let referenceURL = '';
	let referenceNotes = '';
	let referenceMessage = '';

	// Pagination for availableHumans
	let currentPageAvailable = 1;
	let itemsPerPageAvailable = 10;
	$: totalPagesAvailable = Math.max(1, Math.ceil((availableHumans || []).length / itemsPerPageAvailable));
	$: displayedAvailableHumans = (availableHumans || []).slice(
		(currentPageAvailable - 1) * itemsPerPageAvailable,
		currentPageAvailable * itemsPerPageAvailable
	);

	// Debounced search function
	function onSearchInput(event) {
		const value = event.target.value;
		searchQuery = value;
		clearTimeout(searchTimeout);
		searchTimeout = setTimeout(async () => {
			if (searchQuery.trim().length < 1) {
				availableHumans = [];
			} else {
				await handleSearchHumans(Session.SessionId, searchQuery, (results) => {
					availableHumans = results;
					currentPageAvailable = 1; // Reset to first page on new search
				});
			}
		}, 300); // 300ms debounce
	}

	// Sorting for availableHumans
	function sortAvailableHumans(column) {
		if(sortColumnSearch === column) {
			sortDirectionSearch *= -1;
		} else {
			sortColumnSearch = column;
			sortDirectionSearch = 1;
		}
		availableHumans = [...availableHumans].sort((a, b) => {
			let aVal = a[column] || '';
			let bVal = b[column] || '';
			aVal = Array.isArray(aVal) ? aVal.join(' ').toLowerCase() : String(aVal).toLowerCase();
			bVal = Array.isArray(bVal) ? bVal.join(' ').toLowerCase() : String(bVal).toLowerCase();
			return aVal > bVal ? sortDirectionSearch : aVal < bVal ? -sortDirectionSearch : 0;
		});
	}

	// Function to add human to voyage
	async function addHumanToVoyageFromAvailable(human) {
		const roleId = selectedRoleForHuman[human.HumanId];
		if (!roleId) {
			alert("Please select a role for this human before adding.");
			return;
		}

		// Create a human object with the role
		const humanWithRole = {
			...human,
			RoleId: roleId
		};

		await handleSaveVoyageHuman(VoyageId, humanWithRole, setSaveVoyageHuman);

		// Refresh voyageHumans after adding a new human
		await handleGetVoyageHumans(Session.SessionId, VoyageId, setVoyageHumans);
	}

	// Helper function to format birthdate based on accuracy
	function formatBirthDate(date, accuracy) {
		if (!date) return '';
		const mDate = moment(date);
		switch(accuracy) {
			case 'Y': return mDate.format('YYYY');
			case 'M': return mDate.format('YYYY-MM');
			default: return mDate.format('YYYY-MM-DD');
		}
	}

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
				// Use moment with UTC to avoid timezone issues
				Voyage.StartDate = moment.utc(data.StartDate).format("YYYY-MM-DD")||"";
			}
			if (data.EndDate){
				// Use moment with UTC to avoid timezone issues
				Voyage.EndDate = moment.utc(data.EndDate).format("YYYY-MM-DD")||"";
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
	async function setVoyageReferences(data) {
		voyageReferences = data;
	}
	$: {
		formValid = Voyage.ShipId && 
					Voyage.StartLocationId && 
					Voyage.EndLocationId && 
					Voyage.StartDate && Voyage.StartDate !== null && 
					Voyage.EndDate && Voyage.EndDate !== null;
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
			handleGetLocations(Session.SessionId,setLocations)
		]);
		const module = await import('svelecte');
		Svelecte = module.default || module;

		await handleGetLinkReferences(VoyageId, 'voyage', setVoyageReferences);
		isReferencesLoading = false;

		isLoading = false;
	});


	async function saveReferenceForVoyage() {
		referenceMessage = '';
		if (!referenceURL.trim()) {
			referenceMessage = 'URL is required.';
			return;
		}
		const result = await handleSaveReferenceLink({
			LinkId: VoyageId,
			TargetType: 'voyage',
			URL: referenceURL,
			Notes: referenceNotes
		});
		if (result && result.success) {
			referenceMessage = 'Reference added!';
			referenceURL = '';
			referenceNotes = '';
			
			// Refresh the references list
			await handleGetLinkReferences(VoyageId, 'voyage', setVoyageReferences);
		} else {
			referenceMessage = result && result.error ? result.error : 'Error adding reference.';
		}
	}
</script>

<style>
	.truncated-select {
		width: 150px; /* Set a fixed width */
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.clickable-row {
		cursor: pointer;
		transition: background-color 0.2s ease-in-out;
	}

	.clickable-row:hover {
		background-color: #f0f0f0;
	}

	.pagination {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		margin-top: 1rem;
	}

	.pagination button {
		padding: 0.5rem 1rem;
		border: 1px solid #ccc;
		background: white;
		cursor: pointer;
	}

	.pagination button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.pagination span {
		font-weight: bold;
	}
</style>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<div class="ActionBox">


			<form on:submit|preventDefault={async () => {
				if (formValid) {
					await handleSave(Session.SessionId, Voyage, formValid);
				} else {
					alert('Please fill in all required fields: Start Location, End Location, Start Date, and End Date');
				}
			}}>
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
								options={Ships
									.filter((ship, index, self) => 
										index === self.findIndex(s => s.ShipId === ship.ShipId)
									)
									.map(Ship => ({
										value: Ship.ShipId, 
										label: Ship.ShipName
									}))} 
							/>
						</div>
					</div>
				</div>
				<div class="field">
					<label class="label" for="Size">Start Location <span style="color: red;">*</span>
						
					<div class="control">
						<div id="svelecteStartLocation">
							<svelte:component 
								this={Svelecte} 
								bind:value={Voyage.StartLocationId} 
								options={Locations
									.filter((location, index, self) => 
										index === self.findIndex(l => l.LocationId === location.LocationId)
									)
									.map(location => ({
										value: location.LocationId, 
										label: `${location.Address}`
									}))} 
							/>
						</div>
					</div>
				</div>
				
				
				<div class="field">
					<label class="label" for="Size">End Location <span style="color: red;">*</span>
						
					<div class="control">
						<div id="svelecteEndLocation">
							<svelte:component 
								this={Svelecte} 
								bind:value={Voyage.EndLocationId} 
								options={Locations
									.filter((location, index, self) => 
										index === self.findIndex(l => l.LocationId === location.LocationId)
									)
									.map(location => ({
										value: location.LocationId, 
										label: `${location.Address}`
									}))} 
							/>

						</div>

					</div>
				</div>
				<div class="field">
					<label class="label" for="StartDate">Start Date <span style="color: red;">*</span></label>
					<div class="control">
						<input class="input" type="date" id="StartDate" bind:value={Voyage.StartDate} required />
					</div>
				</div>

				<div class="field">
					<label class="label" for="EndDate">End Date <span style="color: red;">*</span></label>
					<div class="control">
						<input class="input" type="date" id="EndDate" bind:value={Voyage.EndDate} required />
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
						<button class="button is-primary" type="submit" disabled={!formValid}>Save</button>
						
					</div>
				</div>

				{#if VoyageId}
				<!-- Available Humans Search Section -->
					<div class="ActionBox">
						<div class="title-container">
							<h3 class="title is-4">Add Humans to Voyage</h3>
						</div>
						
						<!-- Search Box -->
						<div class="field">
							<label for="human-search">Search Available Humans:</label>
							<input
								id="human-search"
								class="input"
								type="text"
								placeholder="Search Humans"
								value={searchQuery}
								on:input={onSearchInput}
								autocomplete="off"
							/>
						</div>

						{#if availableHumans.length > 0}
							<table class="table is-striped is-hoverable is-fullwidth">
								<thead>
									<tr>
										<th on:click={() => sortAvailableHumans('HumanId')}>
											Human ID {sortColumnSearch==='HumanId' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
										</th>
										<th on:click={() => sortAvailableHumans('FirstName')}>
											First Name {sortColumnSearch==='FirstName' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
										</th>
										<th on:click={() => sortAvailableHumans('LastName')}>
											Last Name {sortColumnSearch==='LastName' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
										</th>
										<th on:click={() => sortAvailableHumans('BirthDate')}>
											Birth Date {sortColumnSearch==='BirthDate' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
										</th>
										<th on:click={() => sortAvailableHumans('Roles')}>
											Current Roles {sortColumnSearch==='Roles' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
										</th>
										<th on:click={() => sortAvailableHumans('RacialDescriptor')}>
											Racial Descriptor {sortColumnSearch==='RacialDescriptor' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
										</th>
										<th>Assign Role</th>
										<th>Action</th>
									</tr>
								</thead>
								<tbody>
									{#each displayedAvailableHumans as human}
										<tr class="clickable-row" 
											on:click={() => window.open(`/Admin/Human?HumanId=${human.HumanId}`, '_blank')}
											on:keydown={(e) => {
												if (e.key === 'Enter' || e.key === ' ') {
													e.preventDefault();
													window.open(`/Admin/Human?HumanId=${human.HumanId}`, '_blank');
												}
											}}
											tabindex="0">
											<td>
												<span title={human.HumanId}>
													{human.HumanId ? (human.HumanId.length > 10 ? human.HumanId.substring(0, 15) + '...' : human.HumanId) : ''}
												</span>
											</td>
											<td>{human.FirstName}</td>
											<td>{human.LastName}</td>
											<td>{human.BirthDate ? formatBirthDate(human.BirthDate, human.BirthDateAccuracy) : ''}</td>
											<td>{Array.isArray(human.Roles) && human.Roles.length > 0 ? human.Roles[0] : ''}</td>
											<td>{human.RacialDescriptor}</td>
											<td>
												<select class="input" bind:value={selectedRoleForHuman[human.HumanId]} on:click|stopPropagation>
													<option value="">Select Role</option>
													{#each voyageRoles as role}
														<option value={role.id}>{role.name}</option>
													{/each}
												</select>
											</td>
											<td>
												<button class="button is-primary is-small" type="button" on:click|stopPropagation={() => addHumanToVoyageFromAvailable(human)}>
													Add
												</button>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
							<!-- Pagination controls for available humans -->
							<div class="pagination">
								<button type="button" on:click={() => currentPageAvailable = Math.max(currentPageAvailable - 1, 1)} disabled={currentPageAvailable === 1}>
									Previous
								</button>
								<span>{currentPageAvailable} / {totalPagesAvailable}</span>
								<button type="button" on:click={() => currentPageAvailable = Math.min(currentPageAvailable + 1, totalPagesAvailable)} disabled={currentPageAvailable === totalPagesAvailable}>
									Next
								</button>
							</div>
						{:else if searchQuery.length > 0}
							<p>No humans found matching your search.</p>
						{:else}
							<p>Enter a search term to find humans to add to this voyage.</p>
						{/if}
					</div>
					<div class="ActionBox" style="disabled:true">
						<!-- Enslaved People Table -->
						<div class="title-container">
							<h3 class="title is-2">List of Enslaved People</h3>
							
						</div>
						<table class="ClickableTable" width=100%>
							<thead>
								<tr>
									<th>First Name</th>
									<th>Last Name</th>
									<th>Action</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Enslaved') as Human}
									<tr on:click={() => window.location.href = `/Admin/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
										<td>
											<button class="button is-danger is-small" 
												type="button" 
												style="background-color: #ff3860; color: white; border-color: #ff3860;"
												on:click|stopPropagation={() => {
													if (confirm('Are you sure you want to remove this enslaved person from the voyage?')) {
														handleDeleteVoyageHuman(Session.SessionId, Voyage.VoyageId, Human.HumanId);
													}
												}}>
												🗑️ Remove
											</button>
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
									<th>Action</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Captain') as Human}
									<tr on:click={() => window.location.href = `/Admin/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
										<td>
											<button class="button is-danger is-small" 
												type="button" 
												style="background-color: #ff3860; color: white; border-color: #ff3860;"
												on:click|stopPropagation={() => {
													if (confirm('Are you sure you want to remove this captain from the voyage?')) {
														handleDeleteVoyageHuman(Session.SessionId, Voyage.VoyageId, Human.HumanId);
													}
												}}>
												🗑️ Remove
											</button>
										</td>
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
									<th>Action</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Owner 1') as Human}
									<tr on:click={() => window.location.href = `/Admin/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
										<td>
											<button class="button is-danger is-small" 
												type="button" 
												style="background-color: #ff3860; color: white; border-color: #ff3860;"
												on:click|stopPropagation={() => {
													if (confirm('Are you sure you want to remove this owner from the voyage?')) {
														handleDeleteVoyageHuman(Session.SessionId, Voyage.VoyageId, Human.HumanId);
													}
												}}>
												🗑️ Remove
											</button>
										</td>
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
									<th>Action</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Owner 2') as Human}
									<tr on:click={() => window.location.href = `/Admin/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
										<td>
											<button class="button is-danger is-small" 
												type="button" 
												style="background-color: #ff3860; color: white; border-color: #ff3860;"
												on:click|stopPropagation={() => {
													if (confirm('Are you sure you want to remove this owner from the voyage?')) {
														handleDeleteVoyageHuman(Session.SessionId, Voyage.VoyageId, Human.HumanId);
													}
												}}>
												🗑️ Remove
											</button>
										</td>
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
									<th>Action</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Shipping Agent') as Human}
									<tr on:click={() => window.location.href = `/Admin/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
										<td>
											<button class="button is-danger is-small" 
												type="button" 
												style="background-color: #ff3860; color: white; border-color: #ff3860;"
												on:click|stopPropagation={() => {
													if (confirm('Are you sure you want to remove this shipping agent from the voyage?')) {
														handleDeleteVoyageHuman(Session.SessionId, Voyage.VoyageId, Human.HumanId);
													}
												}}>
												🗑️ Remove
											</button>
										</td>
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
									<th>Action</th>
								</tr>
							</thead>
							<tbody>
								{#each VoyageHumans.filter(h => h.Role === 'Collector Agent') as Human}
									<tr on:click={() => window.location.href = `/Admin/Human?HumanId=${Human.HumanId}`}>
										<td>{Human.FirstName || ''}</td>
										<td>{Human.LastName || ''}</td>
										<td>
											<button class="button is-danger is-small" 
												type="button" 
												style="background-color: #ff3860; color: white; border-color: #ff3860;"
												on:click|stopPropagation={() => {
													if (confirm('Are you sure you want to remove this collector agent from the voyage?')) {
														handleDeleteVoyageHuman(Session.SessionId, Voyage.VoyageId, Human.HumanId);
													}
												}}>
												🗑️ Remove
											</button>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>

					

					<!-- Add Reference Section -->
					<div class="ActionBox">
						<div class="title-container">
							<h3 class="title is-4">Add Reference to this Voyage</h3>
						</div>
						<div class="field">
							<label class="label" for="referenceURL">Reference URL</label>
							<div class="control">
								<input class="input" id="referenceURL" type="text" bind:value={referenceURL} placeholder="Enter reference URL" />
							</div>
						</div>
						<div class="field">
							<label class="label" for="referenceNotes">Notes</label>
							<div class="control">
								<input class="input" id="referenceNotes" type="text" bind:value={referenceNotes} placeholder="Enter notes" />
							</div>
						</div>
						<div class="field">
							<div class="control">
								<button class="button is-primary" type="button" on:click={saveReferenceForVoyage}>Add Reference</button>
							</div>
						</div>
						{#if referenceMessage}
							<div class="notification is-info">{referenceMessage}</div>
						{/if}
					</div>

					<!-- References Table for this Voyage -->
					<div class="ActionBox">
						<div class="title-container">
							<h3 class="title is-4">References Linked to this Voyage</h3>
						</div>
						{#if isReferencesLoading}
							<div>Loading references...</div>
						{:else if voyageReferences.length === 0}
							<div>No references linked to this voyage.</div>
						{:else}
							<table class="table is-striped is-hoverable is-fullwidth">
								<thead>
									<tr>
										<th>URL</th>
										<th>Notes</th>
										<th>Date Updated</th>
									</tr>
								</thead>
								<tbody>
									{#each voyageReferences as reference}
										<tr on:click={() => window.location.href = `/Admin/Reference?ReferenceId=${reference.ReferenceId}`} style="cursor:pointer;">
											<td>{reference.URL}</td>
											<td>{reference.Notes}</td>
											<td>{reference.dateUpdated}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						{/if}
					</div>
				{/if}
			</form>
		</div>
	</div>
{/if}
