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
</style>
<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetHuman } from './handleGetHuman.js';
	import { saveHuman } from './handleSaveHuman.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetHumanLocations } from './handleGetHumanLocations.js';
	import { handleGetHumanFirstParty } from './handleGetHumanFirstParty.js';
	import { handleGetHumanSecondParty } from './handleGetHumanSecondParty.js';
	import { handleGetNotaryTransactions } from './handleGetNotaryTransactions.js';
	import { handleGetEnslavedTransactions } from './handleGetEnslavedTransactions.js';
	import { handleGetCaptains } from './handleGetCaptains.js';
	import { handleMergeHumans } from '../Merge/Humans/handleMergeHumans.js';
	import { handleGetHumanVoyages } from './handleGetHumanVoyages.js';
	import { handleGetFamilies } from './handleGetFamilies.js';
	import { handleGetHumans } from '../Humans/handleGetHumans.js';
	import FamilyTreeCanvas from '../../components/FamilyTreeCanvas.svelte';
	import { handleGetTimelines } from './handleGetTimelines.js';

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

	let mergeHuman = null;
	let isLoading = true;
	let HumanId = null;
	let mergeHumanId = null;
	let locations = [];
	let firstPartyTransactions = [];
	let secondPartyTransactions = [];
	let notaryTransactions = [];
	let enslavedTransactions = [];
	let captainVoyages = [];
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

	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	function formatDateForInput(date) {
		if (!date) return '';
		const d = new Date(date);
		return d.toISOString().split('T')[0]; // Format as YYYY-MM-DD
	}

	onMount(async () => {
		await Session.handleSession();
		HumanId = getURLVariable('HumanId') || null;
		mergeHumanId = getURLVariable('mergeHumanId') || null;
		returnPath = getURLVariable('returnPath');

		if (HumanId) {
			const data = await handleGetHuman(Session.SessionId, HumanId);
			if (data) {
				Human = {
					...data,
					FirstName: data.FirstName || '',
					LastName: data.LastName || '',
					BirthDate: formatDateForInput(data.BirthDate), // Format BirthDate for input
					Roles: data.Roles ? data.Roles.join(', ') : ''
				};
				locations = await handleGetHumanLocations(Session.SessionId, HumanId);
				firstPartyTransactions = await handleGetHumanFirstParty(Session.SessionId, HumanId);
				secondPartyTransactions = await handleGetHumanSecondParty(Session.SessionId, HumanId);
				notaryTransactions = await handleGetNotaryTransactions(Session.SessionId, HumanId);
				enslavedTransactions = await handleGetEnslavedTransactions(Session.SessionId, HumanId);
				captainVoyages = await handleGetCaptains(Session.SessionId, HumanId);
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

		isLoading = false;
	});

	function setHumans(data) {
		Humans = data;
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
		const success = await saveHuman(Session.SessionId, HumanId, Human);
		if (success) {
			window.location.href = returnPath || '/Humans';
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
		const options = { year: 'numeric', month: 'long', day: 'numeric' };
		const dateObj = new Date(date);
		switch (accuracy) {
			case 'Y':
				return dateObj.getFullYear();
			case 'M':
				return dateObj.toLocaleDateString(undefined, { year: 'numeric', month: 'long' });
			case 'D':
				return dateObj.toLocaleDateString(undefined, options);
			default:
				return date;
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
		<a href="/Humans">Back to List</a>
		<h3 class="title is-2">{HumanId ? 'Edit' : 'Add'} Human</h3>

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
				<input id="sex" class="input" type="text" bind:value={Human.Sex} />
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

		{#if families.length > 0}
			<h3 class="title is-3">Family Tree</h3>
			<a href={`/Family?HumanId=${HumanId}`} class="button is-link">Edit Family Tree</a><br/>
			<FamilyTreeCanvas {families} />
		{:else}
			No family relationships defined
		{/if}

		{#if locations.length > 0}
			<h3 class="title is-3">{Human.FirstName} {Human.LastName}'s Timeline</h3>
			<table class="table is-fullwidth is-striped">
				<thead>
					<tr>
						<th>Address</th>
						
						<th>Latitude</th>
						<th>Longitude</th>
						<th>Date Circa</th>
					</tr>
				</thead>
				<tbody>
					{#each locations as location}
						<tr>
							<td>{location.Address}</td>
							
							<td>{location.Latitude}</td>
							<td>{location.Longitude}</td>
							<td>{formatDate(location.Date_Circa, location.Date_Accuracy)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}

		{#if firstPartyTransactions.length > 0}
			<h3 class="title is-3">Transactions where {Human.FirstName} {Human.LastName} is a First Party</h3>
			<table class="table is-fullwidth is-striped">
				<thead>
					<tr>
						<th>Transaction Type</th>
						<th>Date Circa</th>
						<th>First Party</th>
						<th>Second Party</th>
					</tr>
				</thead>
				<tbody>
					{#each firstPartyTransactions as transaction}
						<tr on:click={() => navigateToTransaction(transaction.TransactionId)} style="cursor: pointer;">
							<td>{transaction.TransactionType}</td>
							<td>{formatDate(transaction.date_circa, transaction.date_accuracy)}</td>
							<td>{transaction.FirstPartyFirstName} {transaction.FirstPartyLastName}</td>
							<td>{transaction.SecondPartyFirstName} {transaction.SecondPartyLastName}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}

		{#if secondPartyTransactions.length > 0}
			<h3 class="title is-3">Transactions where {Human.FirstName} {Human.LastName} is a Second Party</h3>
			<table class="table is-fullwidth is-striped">
				<thead>
					<tr>
						<th>Transaction Type</th>
						<th>Date Circa</th>
						<th>First Party</th>
						<th>Second Party</th>
					</tr>
				</thead>
				<tbody>
					{#each secondPartyTransactions as transaction}
						<tr on:click={() => navigateToTransaction(transaction.TransactionId)} style="cursor: pointer;">
							<td>{transaction.TransactionType}</td>
							<td>{formatDate(transaction.date_circa, transaction.date_accuracy)}</td>
							<td>{transaction.FirstPartyFirstName} {transaction.FirstPartyLastName}</td>
							<td>{transaction.SecondPartyFirstName} {transaction.SecondPartyLastName}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}

		{#if notaryTransactions.length > 0}
			<h3 class="title is-3">Transactions where {Human.FirstName} {Human.LastName} is a Notary</h3>
			<table class="table is-fullwidth is-striped">
				<thead>
					<tr>
						<th>Transaction Type</th>
						<th>Date Circa</th>
						<th>First Party</th>
						<th>Second Party</th>
						<th>Notary</th>
					</tr>
				</thead>
				<tbody>
					{#each notaryTransactions as transaction}
						<tr on:click={() => navigateToTransaction(transaction.TransactionId)} style="cursor: pointer;">
							<td>{transaction.TransactionType}</td>
							<td>{formatDate(transaction.date_circa, transaction.date_accuracy)}</td>
							<td>{transaction.FirstPartyFirstName} {transaction.FirstPartyLastName}</td>
							<td>{transaction.SecondPartyFirstName} {transaction.SecondPartyLastName}</td>
							<td>{transaction.NotaryFirstName} {transaction.NotaryLastName}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}

		{#if captainVoyages.length > 0}
			<h3 class="title is-3">Voyages where {Human.FirstName} {Human.LastName} is a Captain</h3>
			<table class="table is-fullwidth is-striped">
				<thead>
					<tr>
						<th>Voyage ID</th>
						<th>Ship ID</th>
						<th>Start Location</th>
						<th>End Location</th>
						<th>Start Date</th>
						<th>End Date</th>
						<th>Notes</th>
					</tr>
				</thead>
				<tbody>
					{#each captainVoyages as voyage}
						<tr on:click={() => navigateToTransaction(voyage.VoyageId)} style="cursor: pointer;">
							<td>{voyage.VoyageId}</td>
							<td>{voyage.ShipId}</td>
							<td>{voyage.StartAddress}</td>
							<td>{voyage.EndAddress}</td>
							<td>{formatDate(voyage.StartDate, 'D')}</td>
							<td>{formatDate(voyage.EndDate, 'D')}</td>
							<td>{voyage.Notes}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}

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

		
	</div>
{/if}
