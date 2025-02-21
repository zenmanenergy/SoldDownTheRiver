<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetTransaction } from './handleGetTransaction.js';
	import { handleGetHumans } from '../Humans/handleGetHumans.js';
	import { handleSaveTransaction } from './handleSaveTransaction.js';
	import { handleDeleteTransaction } from './handleDeleteTransaction.js';
	import { handleGetTransactionHumans } from './handleGetTransactionHumans.js';
	import Select from 'svelte-select';
	import moment from 'moment';

	let transaction = {
		date_circa: '',
		date_accuracy: 'D',
		TransactionType: '',
		NotaryHumanId: '',
		FirstParties: [],
		SecondParties: [],
		LocationId: '',
		TotalPrice: '',
		URL: '',
		notes: '' // New property for transaction notes
	};

	let isLoading = true;
	let transactionId = null;
	let allHumans = [];
	let transactionHumans = [];
	let selectedFirstParty = null;
	let selectedSecondParty = null;
	let selectedNotary = null;

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

				// Ensure FirstParties and SecondParties are parsed correctly
				try {
					transaction.FirstParties = JSON.parse(transaction.FirstParties || "[]");
					transaction.SecondParties = JSON.parse(transaction.SecondParties || "[]");
				} catch (error) {
					console.error("Error parsing parties:", error);
					transaction.FirstParties = [];
					transaction.SecondParties = [];
				}

				// Convert date format
				if (transaction.date_circa) {
					const parsedDate = moment.utc(transaction.date_circa, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);
					if (parsedDate.isValid()) {
						transaction.date_circa = parsedDate.format("YYYY-M-D");
					}
				}
			}
		}

		// Fetch humans and format correctly for `svelte-select`
		await handleGetHumans(Session.SessionId, (data) => {
			if (Array.isArray(data)) {
				allHumans = data.map(h => ({
					value: h.HumanId,
					label: `${h.FirstName} ${h.LastName}`
				}));

				// Set selected Notary
				selectedNotary = allHumans.find(h => h.value === transaction.NotaryHumanId) || null;

				// Set selected First Parties as an array
				selectedFirstParty = transaction.FirstParties.map(fp => 
					allHumans.find(h => h.value === fp.FirstPartyId) || null
				).filter(h => h !== null);

				// Set selected Second Parties as an array
				selectedSecondParty = transaction.SecondParties.map(sp => 
					allHumans.find(h => h.value === sp.SecondPartyId) || null
				).filter(h => h !== null);
			} else {
				console.error("Error: handleGetHumans did not return an array", data);
				allHumans = [];
			}
		});

		// Fetch humans associated with this transaction
		await handleGetTransactionHumans(Session.SessionId, transactionId, (data) => {
			if (Array.isArray(data)) {
				transactionHumans = data;
			} else {
				console.error("Error: handleGetTransactionHumans did not return an array", data);
				transactionHumans = [];
			}
		});

		isLoading = false;
	});

	// Format displayed date based on accuracy
	function getFormattedDate() {
		if (!transaction.date_circa) return "";
		const parts = transaction.date_circa.split("-");
		switch (transaction.date_accuracy) {
			case "D": return transaction.date_circa;
			case "M": return `${parts[0]}-${parts[1]}`;
			case "Y": return `${parts[0]}`;
			default: return transaction.date_circa;
		}
	}

	// Update date when accuracy changes
	function updateDateFormat() {
		transaction.date_circa = getFormattedDate();
	}

	// Helper function to convert centimeters to inches
	function cmToInches(cm) {
		return cm ? (cm / 2.54).toFixed(2) : 'N/A';
	}

	// Helper function to format birthdate based on accuracy
	function formatBirthDate(date, accuracy) {
		if (!date) return 'N/A';
		const mDate = moment(date);
		switch(accuracy) {
			case 'Y': return mDate.format('YYYY');
			case 'M': return mDate.format('YYYY-MM');
			default: return mDate.format('YYYY-MM-DD');
		}
	}

	async function submitTransaction() {
		const transactionData = {
			...transaction,
			FirstParties: JSON.stringify(transaction.FirstParties),
			SecondParties: JSON.stringify(transaction.SecondParties)
		};

		const success = await handleSaveTransaction(Session.SessionId, transactionId, transactionData);
		if (success) {
			window.location.href = '/Transactions';
		} else {
			alert("Failed to save transaction.");
		}
	}

	async function deleteTransaction() {
		if (confirm("Are you sure you want to delete this transaction?")) {
			await handleDeleteTransaction(Session.SessionId, transactionId);
			window.location.href = "/Transactions";
		}
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/Transactions">Back to List</a>
		<h3 class="title is-2">{transactionId ? 'Edit' : 'Add'} Transaction</h3>
		
		<form on:submit|preventDefault={submitTransaction}>
			<!-- Transaction Date -->
			<div class="field">
				<label for="date">Date:</label>
				<input id="date" class="input" type="text" bind:value={transaction.date_circa} on:input={updateDateFormat} placeholder="YYYY-M-D" />
			</div>
		
			<!-- Date Accuracy -->
			<div class="field">
				<label for="date-accuracy">Date Accuracy:</label>
				<select id="date-accuracy" class="input" bind:value={transaction.date_accuracy} on:change={updateDateFormat}>
					<option value="D">Day</option>
					<option value="M">Month</option>
					<option value="Y">Year</option>
				</select>
			</div>
		
			<!-- Notary -->
			<div class="field">
				<label for="notary">Notary:</label>
				{#if allHumans.length > 0}
					<Select id="notary" bind:value={selectedNotary} items={allHumans} />
				{:else}
					<p>Loading humans...</p>
				{/if}
			</div>
			
			<!-- First Parties -->
			<div class="field">
				<label for="first-party">First Parties:</label>
				{#if allHumans.length > 0}
					<Select id="first-party" bind:value={selectedFirstParty} items={allHumans} multiple />
				{:else}
					<p>Loading humans...</p>
				{/if}
			</div>

			<!-- Second Parties -->
			<div class="field">
				<label for="second-party">Second Parties:</label>
				{#if allHumans.length > 0}
					<Select id="second-party" bind:value={selectedSecondParty} items={allHumans} multiple />
				{:else}
					<p>Loading humans...</p>
				{/if}
			</div>
			
			<!-- Notes Field -->
			<div class="field">
				<label for="notes">Notes:</label>
				<textarea id="notes" class="textarea" bind:value={transaction.Notes} placeholder="Enter additional notes"></textarea>
			</div>

			<!-- Buttons -->
			<div class="buttons-container">
				<button class="button is-primary" type="submit">Save</button>
				{#if transactionId} 
					<button class="button is-danger delete-button" type="button" on:click={deleteTransaction}>Delete</button>
				{/if}
			</div>
		</form>

		<!-- Humans Associated with This Transaction -->
		<h4 class="title is-4">Humans Associated with This Transaction</h4>
		<table>
			<thead>
				<tr>
					<th>First Name</th>
					<th>Last Name</th>
					<th>Racial Descriptor</th>
					<th>Sex</th>
					<th>Height (in)</th>
					<th>Physical Features</th>
					<th>Profession</th>
					<th>Birthplace</th>
					<th>Birthdate</th>
				</tr>
			</thead>
			<tbody>
				{#each transactionHumans as human}
					<tr>
						<td>{human.FirstName}</td>
						<td>{human.LastName}</td>
						<td>{human.RacialDescriptor || 'N/A'}</td>
						<td>{human.Sex || 'N/A'}</td>
						<td>{cmToInches(human.Height_cm)}</td>
						<td>{human.physical_features || 'N/A'}</td>
						<td>{human.profession || 'N/A'}</td>
						<td>{human.BirthPlace || 'N/A'}</td>
						<td>{formatBirthDate(human.BirthDate, human.BirthDateAccuracy)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
