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
</style>
<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetHuman } from './handleGetHuman.js';
	import { saveHuman } from './handleSaveHuman.js';
	import { handleDelete } from './handleDelete.js';
	import { handleMergeHumans } from '../Merge/Humans/handleMergeHumans.js';
	import { handleGetHumanVoyages } from './handleGetHumanVoyages.js';
	import { handleGetFamilies } from './handleGetFamilies.js';
	import { handleGetHumans } from '../Humans/handleGetHumans.js';
	import FamilyTreeCanvas from '../../components/FamilyTreeCanvas.svelte';
	import { handleGetTimelines } from './handleGetTimelines.js';
	import { handleGetAKA } from './handleGetAKA.js';
	import { handleSaveAkaName } from './handleSaveAkaName.js';
	import { handleDeleteAkaName } from './handleDeleteAkaName.js';
	import { handleGetTransaction } from '../Transaction/handleGetTransaction.js';
	import { handleGetRoles } from './handleGetRoles.js';
	import { handleSaveTimeline } from './handleSaveTimeline.js';
	import { handleDeleteTimeline } from './handleDeleteTimeline.js';

	let Human = {
		FirstName: '',
		MiddleName: '',
		LastName: '',
		BirthDate: '',
		BirthDateAccuracy: 'd',
		RacialDescriptor: '',
		Sex: '',
		Height_cm: '',
		Roles: ''
	};

	let originalBirthDate = ''; // new variable to store fetched birth date
	let mergeHuman = null;
	let isLoading = true;
	let HumanId = null;
	let mergeHumanId = null;
	let locations = [];
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

	// New variable for the new location/timeline form
	let newLocation = {
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
		Country: ''
	};

	// Updated function to handle saving a timeline using SuperFetch backend
	async function addNewLocation() {
		 // Validate required fields
		if (!newLocation.Latitude || !newLocation.Longitude || !newLocation.Date_Circa) {
			alert("Please enter Latitude, Longitude, and Date Circa.");
			return;
		}
		newLocation.HumanId = HumanId;
		const result = await handleSaveTimeline(Session.SessionId, HumanId, newLocation);
		if(result) {
			locations = [...locations, { ...newLocation, LocationId: result.TimelineId }];
			newLocation = { LocationType: '', Address: '', Latitude: '', Longitude: '', Date_Circa: '', Date_Accuracy: 'D', Name: '', City: '', County: '', State: '', State_abbr: '', Country: '' };
		} else {
			alert("Failed to save timeline.");
		}
	}

	// New function to delete a timeline entry using LocationId
	async function deleteTimeline(locationId) {
		const result = await handleDeleteTimeline(Session.SessionId, HumanId, locationId);
		if(result && result.success) {
			locations = locations.filter(t => t.LocationId !== locationId);
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

	onMount(async () => {
		await Session.handleSession();
		HumanId = getURLVariable('HumanId') || null;
		mergeHumanId = getURLVariable('mergeHumanId') || null;
		returnPath = getURLVariable('returnPath');
		transactionDate = getURLVariable('TransactionDate') || null;

		if (HumanId) {
			const data = await handleGetHuman(Session.SessionId, HumanId);
			if (data) {
				originalBirthDate = formatDateForInput(data.BirthDate); // store the original date
				Human = {
					...data,
					FirstName: data.FirstName || '',
					LastName: data.LastName || '',
					BirthDate: originalBirthDate, // use originalBirthDate
					Roles: data.Roles ? data.Roles.join(', ') : ''
				};
				voyages = await handleGetHumanVoyages(Session.SessionId, HumanId);
				timelines = await handleGetTimelines(Session.SessionId, HumanId);
				if (timelines && timelines.data) {
					locations = timelines.data;
				}
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

		await handleGetHumans(Session.SessionId, setHumans);

		if (Human.Height_cm) {
			Human.Height_in = (Human.Height_cm / 2.54).toFixed(2);
		} else {
			Human.Height_in = '';
		}

		await fetchAKA();

		const TransactionId = getURLVariable('TransactionId');
		if (TransactionId) {
			transactionSummary = await handleGetTransaction(Session.SessionId, TransactionId);
			rolesOptions = await handleGetRoles(Session.SessionId);
		}

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

	async function submitHuman() {
		// Set TransactionId and RoleId on the Human object from the URL and UI input
		const transactionId = getURLVariable('TransactionId') || "";
		if (transactionId) {
			Human.TransactionId = transactionId;
			Human.RoleId = Human.Role;  // assign the selected role as RoleId
		}
		const result = await saveHuman(Session.SessionId, HumanId, Human);
		if (result) {
			const TransactionId = getURLVariable('TransactionId');
			if (TransactionId) {
				window.location.href = `/Transaction?TransactionId=${TransactionId}`;
			} else {
				window.location.href = returnPath || '/Humans';
			}
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
		window.location.href = `/Transaction?TransactionId=${TransactionId}`;
	}

	async function mergeHumans() {
		if (HumanId && mergeHumanId) {
			await handleMergeHumans(Session.SessionId, HumanId, mergeHumanId, (result) => {
				if (result) {
					alert("Humans merged successfully!");
					window.location.href = `/Human?HumanId=${result.HumanId}`;
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
			<h3 class="title is-2">{HumanId ? 'Edit' : 'Add'} Human</h3>

			{#if transactionSummary}
				<div class="transaction-summary">
					<h3 class="title is-3">Transaction Summary</h3>
					<p><strong>Type:</strong> {transactionSummary.TransactionType}</p>
					<p><strong>Date:</strong> {formatDate(transactionSummary.date_circa, transactionSummary.date_accuracy)}</p>
					<p><strong>Buyer:</strong> {transactionSummary.Buyers[0].BuyerFirstName} {transactionSummary.Buyers[0].BuyerLastName}</p>
					<p><strong>Seller:</strong> {transactionSummary.Sellers[0].SellerFirstName} {transactionSummary.Sellers[0].SellerLastName}</p>
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
					<label for="first-name">First Name:</label>
					<input id="first-name" class="input" type="text" bind:value={Human.FirstName} />
				</div>

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
					<input id="racial-descriptor" class="input" type="text" bind:value={Human.RacialDescriptor} />
				</div>

				<div class="field">
					<label for="sex">Sex:</label>
					<select id="sex" class="input" bind:value={Human.Sex}>
						<option value="">Select</option>
						<option value="Male">Male</option>
						<option value="Female">Female</option>
					</select>
				</div>

				

				<div class="field">
					<label for="height-inches">Height (inches):</label>
					<input id="height-inches" class="input" type="number" step="0.01" bind:value={Human.Height_in} min="0" />
				</div>

				<div class="field">
					<label for="roles">Roles (comma-separated):</label>
					<input id="roles" class="input" type="text" bind:value={Human.Roles} placeholder="Role1, Role2, ..." />
				</div>

				<div class="buttons-container">
					<button class="button is-primary" type="submit">Save</button>
					{#if HumanId} 
						<button class="button is-danger delete-button" type="button" on:click={deleteHuman}>Delete</button>
					{/if}
				</div>
			</form>

			{#if akaNames.length > 0}
				<h3 class="title is-3">Also Known As (AKA)</h3>
				<table class="table is-fullwidth is-striped">
					<thead>
						<tr>
							<th>First Name</th>
							<th>Middle Name</th>
							<th>Last Name</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each akaNames as aka}
							<tr>
								<td>{aka.AKAFirstName}</td>
								<td>{aka.AKAMiddleName}</td>
								<td>{aka.AKALastName}</td>
								<td>
									<button class="button is-danger" on:click={() => handleDeleteAkaName(Session.SessionId, aka.AKAHumanId, HumanId)}>Delete</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}

			<h3 class="title is-3">Add New AKA</h3>
			<form on:submit|preventDefault={() => handleSaveAkaName(Session.SessionId, null, HumanId, newAKA.AKAFirstName, newAKA.AKAMiddleName, newAKA.AKALastName, true)}>
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
				<button class="button is-primary" type="submit">Add AKA</button>
			</form>

			{#if families.length > 0}
				<h3 class="title is-3">Family Tree</h3>
				<a href={`/Family?HumanId=${HumanId}`} class="button is-link">Edit Family Tree</a><br/>
				<FamilyTreeCanvas {families} />
			{:else}
				No family relationships defined
			{/if}

			
			<h3 class="title is-3">{Human.FirstName} {Human.LastName}'s Timeline</h3>
			<table class="table is-fullwidth is-striped">
				<thead>
					<tr>
						<th>Type</th>
						<th>Address</th>
						<th>Latitude</th>
						<th>Longitude</th>
						<th>Date Circa</th>
						<th>Date Accuracy</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{#if locations.length > 0}
						{#each locations as location}
							<tr>
								<td>{location.LocationType || ''}</td>
								<td>{location.Address || ''}</td>
								<td>{location.Latitude || ''}</td>
								<td>{location.Longitude || ''}</td>
								<td>{formatDate(location.Date_Circa, location.Date_Accuracy)}</td>
								<td>{location.Date_Accuracy || 'D'}</td>
								<td>
									<button class="button is-danger" on:click={() => deleteTimeline(location.LocationId)}>Delete</button>
								</td>
							</tr>
						{/each}
					{/if}
					<tr>
						<td>
							<input class="input" type="text" bind:value={newLocation.LocationType} placeholder="Type..." />
						</td>
						<td>
							<input class="input" type="text" bind:value={newLocation.Address} placeholder="Address..." />
						</td>
						<td>
							<input class="input" type="number" bind:value={newLocation.Latitude} placeholder="Latitude..." />
						</td>
						<td>
							<input class="input" type="number" bind:value={newLocation.Longitude} placeholder="Longitude..." />
						</td>
						<td>
							<input class="input" type="date" bind:value={newLocation.Date_Circa} placeholder="Date Circa..." />
						</td>
						<td>
							<select class="input" bind:value={newLocation.Date_Accuracy}>
								<option value="D">D</option>
								<option value="M">M</option>
								<option value="Y">Y</option>
							</select>
						</td>
						<td>
							<button class="button is-primary" type="button" on:click={addNewLocation}>Save</button>
						</td>
					</tr>
				</tbody>
			</table>

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
							<tr on:click={() => window.location.href = `/Voyage?VoyageId=${voyage.VoyageId}`} style="cursor: pointer;">
								<td>{voyage.VoyageId}</td>
								<td>{voyage.RoleId}</td>
								<td>{voyage.Notes}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}

		</form>
		</div>
	</div>
{/if}
