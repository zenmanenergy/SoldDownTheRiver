<style>
	.table tbody tr:hover {
		background-color: #f0f0f0;
	}
	.merge-box {
		border: 2px solid #ffcc00;
		padding: 10px;
		background-color: #fff8e1;
		margin-bottom: 20px;
	}
	.merge-box h3 {
		margin-top: 0;
	}
	.transaction-summary {
		border: 1px solid #ccc;
		padding: 15px;
		margin-bottom: 20px;
		background-color: #f9f9f9;
	}
	.merge-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.7);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 9999;
	}
	.merge-message {
		background-color: white;
		padding: 30px;
		border-radius: 10px;
		text-align: center;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}
	.merge-spinner {
		border: 4px solid #f3f3f3;
		border-top: 4px solid #3498db;
		border-radius: 50%;
		width: 40px;
		height: 40px;
		animation: spin 1s linear infinite;
		margin: 0 auto 15px;
	}
	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
<script>
	import { onMount } from 'svelte';
	import {Session} from "../../Session.js";
	import { handleGetHuman } from './handleGetHuman.js';
	import { saveHuman } from './handleSaveHuman.js';
	import { handleDelete } from './handleDelete.js';
	import { handleMergeHumans } from '../Merge/Humans/handleMergeHumans.js';
	import { handleGetHumanVoyages } from './handleGetHumanVoyages.js';
	import { handleGetFamilies } from './handleGetFamilies.js';
	import FamilyTreeCanvas from '../../../components/FamilyTreeCanvas.svelte';
	import { handleGetTimelines } from './handleGetTimelines.js';
	import { handleGetAKA } from './handleGetAKA.js';
	import { handleSaveAkaName } from './handleSaveAkaName.js';
	import { handleDeleteAkaName } from './handleDeleteAkaName.js';
	import { handleGetTransaction } from '../Transaction/handleGetTransaction.js';
	import { handleGetHumanTransactions } from './handleGetHumanTransactions.js';
	import { handleGetRoles } from './handleGetRoles.js';
	import { handleSaveTimeline } from './handleSaveTimeline.js';
	import { handleDeleteTimeline } from './handleDeleteTimeline.js';
	import { handleGetLocations } from '../Locations/handleGetLocations.js';
	import { handleGetRacialDescriptors } from './handleGetRacialDescriptors.js';

	let Svelecte;
	let Human = {
		FirstName: '',
		MiddleName: '',
		LastName: '',
		isCompany: '',
		BirthDate: '',
		BirthDateAccuracy: 'd',
		RacialDescriptor: '',
		Sex: '',
		Height_cm: '',
		DateUpdated: '', // new field for last update timestamp
		isApproved: false
	};

	let originalBirthDate = ''; // new variable to store fetched birth date
	let mergeHuman = null;
	let isLoading = true;
	let HumanId = null;
	let mergeHumanId = null;
	let Locations = [];
	let voyages = [];
	let families = [];
	let returnPath;
	let Humans = [];
	let filteredHumans = [];
	let searchQuery = '';
	let selectedHumanId = null;
	let relationshipType = '';
	let relationshipOptions = ['Husband', 'Wife', 'Son', 'Daughter', 'Father', 'Mother', 'Brother', 'Sister'];
	let timelines = [];
	let akaNames = [];
	let newAKA = { AKAFirstName: '', AKAMiddleName: '', AKALastName: '' };
	let transactionSummary = null;
	let rolesOptions = [];

	let transactionDate = null;
	let ageYears = '';
	let ageMonths = '';
	let isMerging = false; // Loading state for merge operation

	// New variable for storing transactions
	let transactions = [];

	// New variable for the new location/timeline form
	let NewTimeline = {
		LocationType: '',
		Address: '',
		Latitude: '',
		Longitude: '',
		Date_Circa: '',
		Date_Accuracy: 'D',
		Name: '',
		City: '',
		County: '',
		State: '',
		State_abbr: '',
		Country: '',
		RoleId: ''
	};
	async function setLocations(data) {
		// Locations = [{HumanId: "add_new", City: "[Add New]", State: ""}, ...data];
		Locations=data
	}
	// Updated function to handle saving a timeline using SuperFetch backend
	async function addNewTimeline() {
		 // Validate required fields
		if (!NewTimeline.LocationId || !NewTimeline.Date_Circa) {
			alert("Please enter Location and Date Circa.");
			return;
		}
		NewTimeline.HumanId = HumanId;
		const result = await handleSaveTimeline(Session.SessionId, HumanId, NewTimeline);
		if (result) {
			timelines = [...timelines, { ...NewTimeline, LocationId: result.TimelineId }];
			NewTimeline = { LocationType: '', LocationId: '', Date_Circa: '', Date_Accuracy: 'D', RoleId: ''};
			window.location.href = `/Admin/Human?HumanId=${HumanId}`;
		} else {
			alert("Failed to save timeline.");
		}
	}

	// New function to delete a timeline entry using LocationId
	async function deleteTimeline(locationId) {
		const result = await handleDeleteTimeline(Session.SessionId, HumanId, locationId);
		if(result && result.success) {
			timelines = timelines.filter(t => t.LocationId !== locationId); // changed variable from locations to timelines
		} else {
			alert("Failed to delete timeline.");
		}
	}

	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	function formatDateForInput(date) {
		if (!date) return '';
		const d = new Date(date);
		return d.toISOString().split('T')[0]; // Format as YYYY-MM-DD
	}

	function calculateBirthDate() {
		if (!transactionSummary?.date_circa || (ageYears === '' && ageMonths === '')) {
			return originalBirthDate;
		}
		// Create a date using the transaction date string without appending extra text
		let baseDate = new Date(transactionSummary.date_circa);
		if (isNaN(baseDate)) {
			return originalBirthDate;
		}
		let years = parseInt(ageYears) || 0;
		let months = parseInt(ageMonths) || 0;
		baseDate.setUTCFullYear(baseDate.getUTCFullYear() - years);
		baseDate.setUTCMonth(baseDate.getUTCMonth() - months);
		return baseDate.toISOString().split('T')[0];
	}

	$: Human.BirthDate = (ageYears === '' && ageMonths === '') ? originalBirthDate : calculateBirthDate();
	// $: console.log("Updated Human BirthDate:", Human.BirthDate, "ageYears:", ageYears, "ageMonths:", ageMonths, "transaction date:", transactionSummary ? transactionSummary.date_circa : 'N/A');
	
	function handleLocationSelection(event) {
		if (event.target.value.length<=1){
			Query=event.target.value
			handleGetCaptains(Session.SessionId, Query, setCaptains)
		}
	}
	let racialDescriptors = []; // New variable to store racial descriptors

	onMount(async () => {
		await Session.handleSession();
		HumanId = getURLVariable('HumanId') || null;
		mergeHumanId = getURLVariable('mergeHumanId') || null;
		returnPath = getURLVariable('returnPath');
		transactionDate = getURLVariable('TransactionDate') || null;

		const module = await import('svelecte');
		Svelecte = module.default || module;
		
		Promise.resolve().then(() => {
			const svelecteLocation = document.querySelector('#svelecteLocation');
			if (svelecteLocation) {
				const svelecteLocationSearch = svelecteLocation.querySelector('input');
				if (svelecteLocationSearch) {
					svelecteLocationSearch.addEventListener('input', handleLocationInput);
				}
			}
		});
		if (HumanId) {
			const data = await handleGetHuman(Session.SessionId, HumanId);
			if (data) {
				originalBirthDate = formatDateForInput(data.BirthDate); // store the original date
				Human = {
					...data,
					FirstName: data.FirstName || '',
					LastName: data.LastName || '',
					BirthDate: originalBirthDate, // use originalBirthDate
					isCompany: data.isCompany || '',
					isApproved: data.isApproved || false
				};
				voyages = await handleGetHumanVoyages(Session.SessionId, HumanId);
				let _timelines = await handleGetTimelines(Session.SessionId, HumanId);
				
				if (_timelines && _timelines.data) {
					timelines = _timelines.data;
				}
			}
			const humanTransactions = await handleGetHumanTransactions(Session.SessionId, HumanId);
			console.log(humanTransactions);
			if (humanTransactions){
				transactions = humanTransactions;
			}
		}

		if (mergeHumanId) {
			mergeHuman = await handleGetHuman(Session.SessionId, mergeHumanId);
			if (mergeHuman) {
				mergeHuman.FirstName = mergeHuman.FirstName || '';
				mergeHuman.LastName = mergeHuman.LastName || '';
			}
		}

		await handleGetFamilies(Session.SessionId, HumanId, (data) => {
			if (data) {
				families = data;
			}
		});

		

		if (Human.Height_cm) {
			Human.Height_in = (Human.Height_cm / 2.54).toFixed(2);
		} else {
			Human.Height_in = '';
		}

		await fetchAKA();

		const TransactionId = getURLVariable('TransactionId');
		if (TransactionId) {
			transactionSummary = await handleGetTransaction(Session.SessionId, TransactionId);
		}
		
		// Always fetch roles for timeline functionality
		rolesOptions = await handleGetRoles(Session.SessionId);
		
		handleGetLocations(Session.SessionId,setLocations),
		racialDescriptors = await handleGetRacialDescriptors(Session.SessionId);
		isLoading = false;
	});

	function setHumans(data) {
		Humans = data;
	}

	async function fetchAKA() {
		if (HumanId) {
			await handleGetAKA(Session.SessionId, HumanId, (data) => {
				akaNames = data || [];
			});
		}
	}

	$: {
		filteredHumans = Humans.filter(human => {
			const search = searchQuery.toLowerCase();
			const values = [
				human.FirstName,
				human.MiddleName,
				human.LastName
			];
			return values.some(value => value && value.toLowerCase().includes(search));
		});
	}

	// Helper function to generate a timestamp in EST as "YYYY-MM-DD HH:mm:ss"
	function getESTFormattedTimestamp() {
		// Get local time in America/New_York from the built-in API
		const nowEST = new Date().toLocaleString('en-US', { timeZone: 'America/New_York', hour12: false });
		// nowEST is in "MM/DD/YYYY, HH:MM:SS" format
		const [datePart, timePart] = nowEST.split(', ');
		const [month, day, year] = datePart.split('/');
		return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')} ${timePart}`;
	}

	async function submitHuman() {
		// Set TransactionId and RoleId on the Human object from the URL and UI input
		const transactionId = getURLVariable('TransactionId') || "";
		if (transactionId) {
			Human.TransactionId = transactionId;
			Human.RoleId = Human.Role; // assign the selected role as RoleId

			// Ensure RoleId is selected
			if (!Human.RoleId) {
				alert("Role is required when a transaction is associated.");
				return;
			}
		}
		const result = await saveHuman(Session.SessionId, HumanId, Human);
		if (result) {
			// Update DateUpdated using the EST timestamp
			// Human.DateUpdated = getESTFormattedTimestamp();
			const TransactionId = getURLVariable('TransactionId');
			console.log(result)
			
			window.location.href = `/Admin/Human?HumanId=${result.HumanId}`;
		} else {
			alert("Failed to save human.");
		}
	}

	async function deleteHuman() {
		if (confirm("Are you sure you want to delete this human? This action cannot be undone.")) {
			await handleDelete(Session.SessionId, HumanId);
		}
	}

	async function submitRelationship() {
		if (!selectedHumanId || !relationshipType) {
			alert('Please select a human and a relationship type.');
			return;
		}

		const response = await fetch('/Family/AddRelationship', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				SessionId: Session.SessionId,
				HumanId: selectedHumanId,
				RelationshipType: relationshipType
			})
		});

		if (response.ok) {
			alert('Relationship added successfully!');
			window.location.reload();
		} else {
			alert('Failed to add relationship.');
		}
	}

	function formatDate(date, accuracy) {
		const d = new Date(date);
		if (isNaN(d)) return "";
		if (accuracy === "M") {
			return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2);
		} else if (accuracy === "Y") {
			return d.getFullYear().toString();
		} else { // Default "D"
			return d.toISOString().split('T')[0];
		}
	}

	function navigateToTransaction(TransactionId) {
		window.location.href = `/Admin/Transaction?TransactionId=${TransactionId}`;
	}

	async function mergeHumans() {
		if (HumanId && mergeHumanId) {
			isMerging = true; // Show loading overlay
			await handleMergeHumans(Session.SessionId, HumanId, mergeHumanId, (result) => {
				isMerging = false; // Hide loading overlay
				if (result) {
					alert("Humans merged successfully!");
					window.location.href = `/Admin/Human?HumanId=${result.HumanId}`;
				} else {
					alert("Failed to merge humans.");
				}
			});
		} else {
			alert("Both HumanId and mergeHumanId are required to merge humans.");
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
				<h3 class="title is-3">{HumanId ? 'Edit' : 'Add'} Human</h3>
				{#if HumanId} 
					<button class="button is-danger delete-button" type="button" on:click={deleteHuman}>Delete</button>
				{/if}
			</div>

			{#if transactionSummary}
				<div class="transaction-summary">
					<h3 class="title is-3">Transaction Summary</h3>
					<a target="_blank" href="/Transaction?TransactionId={transactionSummary.TransactionId}">View</a>
					<p><strong>Type:</strong> {transactionSummary.TransactionType}</p>
					<p><strong>Date:</strong> {formatDate(transactionSummary.date_circa, transactionSummary.date_accuracy)}</p>
					<p><strong>Buyer:</strong> {transactionSummary.Buyers[0].BuyerFirstName || ''} {transactionSummary.Buyers[0].BuyerLastName || ''}</p>
					<p><strong>Seller:</strong> {transactionSummary.Sellers[0].SellerFirstName || ''} {transactionSummary.Sellers[0].SellerLastName || ''}</p>
				</div>
			{/if}

			{#if mergeHuman}
				<div class="merge-box">
					<h3 class="title is-3">Merge Human</h3>
					<table class="table is-fullwidth is-striped">
						<thead>
							<tr>
								<th>First Name</th>
								<th>Last Name</th>
							</tr>
						</thead>
						<tbody>
							<tr>
								<td>{mergeHuman.FirstName}</td>
								<td>{mergeHuman.LastName}</td>
							</tr>
						</tbody>
					</table>
					<button class="button is-warning" on:click={mergeHumans}>Merge These Humans</button>
				</div>
			{/if}
			
			<form on:submit|preventDefault={submitHuman}>
				<div class="field">
					<label for="isCompany">Individual or Company?</label>
					<select id="isCompany" class="input" bind:value={Human.isCompany}>
						<option value="1">Company</option> <!-- Ensure value is a string -->
						<option value="">Individual</option>
					</select>
				</div>

				<div class="field">
					{#if Human.isCompany == ""} <!-- Use loose equality to handle potential type mismatches -->
						<label for="first-name">First Name:</label>
					{:else}
						<label for="first-name">Company Name:</label>
					{/if}
					<input id="first-name" class="input" type="text" bind:value={Human.FirstName} />
				</div>

				{#if Human.isCompany == ""}
					<div class="field">
						<label for="middle-name">Middle Name:</label>
						<input id="middle-name" class="input" type="text" bind:value={Human.MiddleName} />
					</div>

					<div class="field">
						<label for="last-name">Last Name:</label>
						<input id="last-name" class="input" type="text" bind:value={Human.LastName} />
					</div>

					{#if transactionSummary}
						<div class="field">
							<label for="role-select">Role:</label>
							<select id="role-select" class="input" bind:value={Human.Role}>
								<option value=""></option>
								{#each rolesOptions as role}
									<option value={role.RoleId}>{role.Role}</option>
								{/each}
							</select>
						</div>
						<div class="field">
							<label for="age-years">Age (years):</label>
							<input id="age-years" class="input" type="number" bind:value={ageYears} min="0" />
						</div>
						<div class="field">
							<label for="age-months">Age (months):</label>
							<input id="age-months" class="input" type="number" bind:value={ageMonths} min="0" max="11" />
						</div>
					{/if}

					<div class="field">
						<label for="birth-date">Birth Date:</label>
						<input id="birth-date" class="input" type="date" bind:value={Human.BirthDate} />
					</div>

					<div class="field">
						<label for="birth-accuracy">Birth Date Accuracy:</label>
						<select id="birth-accuracy" class="input" bind:value={Human.BirthDateAccuracy}>
							<option value="d">Day</option>
							<option value="m">Month</option>
							<option value="y">Year</option>
						</select>
					</div>

					<div class="field">
						<label for="racial-descriptor">Racial Descriptor:</label>
						<select id="racial-descriptor" class="input" bind:value={Human.RacialDescriptor}>
							<option value="">Select</option>
							{#each racialDescriptors as descriptor}
								<option value={descriptor}>{descriptor}</option>
							{/each}
						</select>
					</div>

					<div class="field">
						<label for="sex">Sex:</label>
						<select id="sex" class="input" bind:value={Human.Sex}>
							<option value="">Select</option>
							<option value="Male">Male</option>
							<option value="Female">Female</option>
							<option value="Unknown">Unknown</option>
						</select>
					</div>

					<div class="field">
						<label for="height-inches">Height (inches):</label>
						<input id="height-inches" class="input" type="number" step="0.01" bind:value={Human.Height_in} min="0" />
					</div>
				{/if}

				<h4 class="title is-4">Reviewer ONLY:</h4>
				<!-- isApproved Checkbox -->
				<div class="field">
					<label class="checkbox">
						<input type="checkbox" bind:checked={Human.isApproved} />
						Approved
					</label>
				</div>

				<div class="buttons-container">
					<button class="button is-primary" type="submit">Save</button>
					{#if Human.DateUpdated}
						<span style="margin-left: 1rem;">Last Updated: {Human.DateUpdated}</span>
					{/if}
					
				</div>
			</form>

			{#if HumanId}
				<br/>
				<div class="ActionBox">
					{#if akaNames.length > 0}
						<h3 class="title is-3">Also Known As (AKA)</h3>
						<table class="table is-fullwidth is-striped">
							<thead>
								<tr>
									{#if Human.isCompany == ""}
										<th>First Name</th>
										<th>Middle Name</th>
										<th>Last Name</th>
									{:else}
										<th>Company</th>
									{/if}
									<th>Actions</th>
								</tr>
							</thead>
							<tbody>
								{#each akaNames as aka}
									<tr>
										{#if Human.isCompany == ""}
											<td>{aka.AKAFirstName}</td>
											<td>{aka.AKAMiddleName}</td>
											<td>{aka.AKALastName}</td>
										{:else}
											<td>{aka.AKAFirstName}</td>
										{/if}
										<td>
											<button class="button is-danger" on:click={() => handleDeleteAkaName(Session.SessionId, aka.AKAHumanId, HumanId)}>Delete</button>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					{/if}
			
					<h3 class="title is-3">Add New AKA (Also Known As)</h3>
					<form on:submit|preventDefault={() => handleSaveAkaName(Session.SessionId, null, HumanId, newAKA.AKAFirstName, newAKA.AKAMiddleName, newAKA.AKALastName, true)}>
						{#if Human.isCompany == ""}
							<div class="field">
								<label for="aka-first-name">First Name:</label>
								<input id="aka-first-name" class="input" type="text" bind:value={newAKA.AKAFirstName} />
							</div>
							<div class="field">
								<label for="aka-middle-name">Middle Name:</label>
								<input id="aka-middle-name" class="input" type="text" bind:value={newAKA.AKAMiddleName} />
							</div>
							<div class="field">
								<label for="aka-last-name">Last Name:</label>
								<input id="aka-last-name" class="input" type="text" bind:value={newAKA.AKALastName} />
							</div>
						{:else}
							<div class="field">
								<label for="aka-first-name">Company:</label>
								<input id="aka-first-name" class="input" type="text" bind:value={newAKA.AKAFirstName} />
							</div>
						{/if}
						<button class="button is-primary" type="submit">Add AKA</button>
					</form>

				</div>
				
				{#if families.length > 0}
					<h3 class="title is-3">Family Tree</h3>
					<a href={`/Admin/Family?HumanId=${HumanId}`} class="button is-link">Edit Family Tree</a><br/>
					<FamilyTreeCanvas {families} BaseHref="/Admin/Human" />
				{:else}
					No family relationships defined
				{/if}
				<br/>
				<div class="ActionBox">
					{#if timelines.length > 0}
						<h3 class="title is-3">{Human.FirstName} {Human.LastName}'s Timeline</h3>
						<table class="table is-fullwidth is-striped">
							<thead>
								<tr>
									<th>Location Type/Name</th>
									<th>Location</th>
									<th>Latitude,Longitude</th>
									<th>Date Circa</th>
									<th>Role</th>
									<th>Actions</th>
								</tr>
							</thead>
							<tbody>
							
								{#each timelines as timeline}
										<tr on:click={() => window.open(`/Admin/Location?LocationId=${timeline.LocationId}`, '_blank')} style="cursor: pointer;">
										<td>{timeline.LocationType || ''}</td>
										<td>{timeline.Address || ''}</td>
										<td>{timeline.Latitude || ''},{timeline.Longitude || ''}</td>
										<td>{formatDate(timeline.Date_Circa, timeline.Date_Accuracy)}</td>
										<td>{rolesOptions.find(role => role.RoleId === timeline.RoleId)?.Role || ''}</td>
										<td>
											<button class="button is-danger" on:click|stopPropagation={() => deleteTimeline(timeline.LocationId)}>Delete</button>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					{/if}
					<form>
					<h3 class="title is-3">Add a Timeline Event</h3>
					<div class="field">
						<label class="label" for="Size">Location Type/Name</label>
						<div class="control">
							<input class="input" type="text" bind:value={NewTimeline.LocationType} placeholder="Type..." />
						</div>
					</div>
					<div class="field">
						<label class="label" for="Size">Location</label>
						<div class="control">
							<svelte:component 
								this={Svelecte} 
								bind:value={NewTimeline.LocationId} 
								on:input={handleLocationSelection} 
								options={Locations.map(location => ({
									value: location.LocationId, 
									label: `${location.Address}`
								}))} 
							/>
						</div>
					</div>
					<div class="field">
						<label class="label" for="Size">Date Circa</label>
						<div class="control">
							<input class="input" type="date" bind:value={NewTimeline.Date_Circa} placeholder="Date Circa..." />
						</div>
					</div>
					<div class="field">
						<label class="label" for="Size">Date accuracy</label>
						<div class="control">
							<select class="input" bind:value={NewTimeline.Date_Accuracy}>
								<option value="D">Day</option>
								<option value="M">Month</option>
								<option value="Y">Year</option>
							</select>
						</div>
					</div>
					<div class="field">
						<label class="label" for="role-select">Role</label>
						<div class="control">
							<select class="input" bind:value={NewTimeline.RoleId}>
								<option value="">Select Role</option>
								{#each rolesOptions as role}
									<option value={role.RoleId}>{role.Role}</option>
								{/each}
							</select>
						</div>
					</div>
					<button class="button is-primary" type="button" on:click={addNewTimeline}>Save</button>
				</form>
				</div>
				{#if voyages.length > 0}
					<h3 class="title is-3">Voyages involving {Human.FirstName} {Human.LastName}</h3>
					<table class="table is-fullwidth is-striped">
						<thead>
							<tr>
								<th>Voyage ID</th>
								<th>Role ID</th>
								<th>Notes</th>
							</tr>
						</thead>
						<tbody>
							{#each voyages as voyage}
								<tr on:click={() => window.location.href = `/Admin/Voyage?VoyageId=${voyage.VoyageId}`} style="cursor: pointer;">
									<td>{voyage.VoyageId}</td>
									<td>{voyage.RoleId}</td>
									<td>{voyage.Notes}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{/if}

				<!-- New Transactions List Section -->
				{#if transactions.length > 0}
					<div class="ActionBox">
						<h3 class="title is-3">Transactions</h3>
						<!-- Replacing old list with a table -->
						<table class="table is-fullwidth is-striped">
							<thead>
								<tr>
									<th>TransactionType</th>
									<th>Date Circa</th>
									<th>Notary</th>
									<th>Sellers</th>
									<th>Buyers</th>
								</tr>
							</thead>
							<tbody>
								{#each transactions as txn}
									<tr on:click={() => window.open(`/Admin/Transaction?TransactionId=${txn.TransactionId}`, '_blank')} style="cursor: pointer;">
										<td>{txn.TransactionType || ''}</td>
										<td>{formatDate(txn.date_circa, txn.date_accuracy) || ''}</td>
										<td>{txn.Notary || ''}</td>
										<td>{txn.Sellers || ''}</td>
										<td>{txn.Buyers || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/if}
			{/if}

		</form>
		</div>
	</div>
{/if}

<!-- Merge Loading Overlay -->
{#if isMerging}
	<div class="merge-overlay">
		<div class="merge-message">
			<div class="merge-spinner"></div>
			<h3>Merging Humans...</h3>
			<p>Please wait while we merge the selected humans. This may take a moment.</p>
		</div>
	</div>
{/if}
