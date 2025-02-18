<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetTransaction } from './handleGetTransaction.js';
	import { saveTransaction } from './handleSaveTransaction.js';
	import { handleDeleteTransaction } from './handleDeleteTransaction.js';

	let transaction = {
		date_circa: '',
		date_accuracy: 'd',
		TransactionType: '',
		NotaryHumanId: '',
		FirstPartyId: '',
		SecondPartyId: '',
		LocationId: '',
		TotalPrice: '',
		URL: ''
	};

	let isLoading = true;
	let transactionId = null;
	let allHumans = [];
	let allLocations = [];
	let searchFirstParty = "", searchSecondParty = "", searchNotary = "", searchLocation = "";

	// Get TransactionId from URL
	function getTransactionIdFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("TransactionId") || null;
	}

	onMount(async () => {
		await Session.handleSession();
		transactionId = getTransactionIdFromURL();

		if (transactionId) {
			const data = await handleGetTransaction(Session.SessionId, transactionId);
			if (data) {
				transaction = { ...data };
			}
		}

		// Fetch all humans and locations
		await fetchHumans();
		await fetchLocations();

		isLoading = false;
	});

	async function fetchHumans() {
		const response = await fetch('/api/humans');
		allHumans = await response.json();
	}

	async function fetchLocations() {
		const response = await fetch('/api/locations');
		allLocations = await response.json();
	}

	async function submitTransaction() {
		const success = await saveTransaction(Session.SessionId, transactionId, transaction);
		if (success) {
			window.location.href = '/Transactions'; // Redirect after saving
		} else {
			alert("Failed to save transaction.");
		}
	}

	async function deleteTransaction() {
		if (confirm("Are you sure you want to delete this transaction? This action cannot be undone.")) {
			await handleDeleteTransaction(Session.SessionId, transactionId);
		}
	}

	// Filter humans based on search
	$: filteredHumans = allHumans.filter(human =>
		(`${human.FirstName} ${human.LastName}`).toLowerCase().includes(searchFirstParty.toLowerCase())
	);

	$: filteredLocations = allLocations.filter(loc =>
		(`${loc.Address} ${loc.City} ${loc.County} ${loc.State_abbr}`).toLowerCase().includes(searchLocation.toLowerCase())
	);
</script>

<style>
	.buttons-container {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
	}

	.delete-button {
		margin-left: auto;
	}
</style>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/Transactions">Back to List</a>
		<h3 class="title is-2">{transactionId ? 'Edit' : 'Add'} Transaction</h3>
		
		<form on:submit|preventDefault={submitTransaction}>
			<div class="field">
				<label for="date">Date:</label>
				<input id="date" class="input" type="date" bind:value={transaction.date_circa} />
			</div>

			<div class="field">
				<label for="transaction-type">Transaction Type:</label>
				<input id="transaction-type" class="input" type="text" bind:value={transaction.TransactionType} />
			</div>

			<div class="field">
				<label for="notary-search">Notary:</label>
				<input id="notary-search" class="input" type="text" placeholder="Search Notary..." bind:value={searchNotary} />
				<select id="notary" class="input" bind:value={transaction.NotaryHumanId}>
					{#each filteredHumans as human}
						<option value={human.HumanId}>{human.FirstName} {human.LastName}</option>
					{/each}
				</select>
			</div>

			<div class="field">
				<label for="first-party-search">First Party:</label>
				<input id="first-party-search" class="input" type="text" placeholder="Search First Party..." bind:value={searchFirstParty} />
				<select id="first-party" class="input" bind:value={transaction.FirstPartyId}>
					{#each filteredHumans as human}
						<option value={human.HumanId}>{human.FirstName} {human.LastName}</option>
					{/each}
				</select>
			</div>

			<div class="field">
				<label for="second-party-search">Second Party:</label>
				<input id="second-party-search" class="input" type="text" placeholder="Search Second Party..." bind:value={searchSecondParty} />
				<select id="second-party" class="input" bind:value={transaction.SecondPartyId}>
					{#each filteredHumans as human}
						<option value={human.HumanId}>{human.FirstName} {human.LastName}</option>
					{/each}
				</select>
			</div>

			<div class="field">
				<label for="location-search">Location:</label>
				<input id="location-search" class="input" type="text" placeholder="Search Location..." bind:value={searchLocation} />
				<select id="location" class="input" bind:value={transaction.LocationId}>
					{#each filteredLocations as loc}
						<option value={loc.LocationId}>{loc.Address}, {loc.City}, {loc.County}, {loc.State_abbr}</option>
					{/each}
				</select>
			</div>

			<div class="field">
				<label for="total-price">Total Price:</label>
				<input id="total-price" class="input" type="number" bind:value={transaction.TotalPrice} step="0.01" />
			</div>

			<div class="field">
				<label for="transaction-url">URL:</label>
				<input id="transaction-url" class="input" type="text" bind:value={transaction.URL} />
			</div>

			<div class="buttons-container">
				<button class="button is-primary" type="submit">Save</button>
				{#if transactionId} 
					<button class="button is-danger delete-button" type="button" on:click={deleteTransaction}>Delete</button>
				{/if}
			</div>
		</form>
	</div>
{/if}
