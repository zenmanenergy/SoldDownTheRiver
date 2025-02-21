<style>
	.clickable-row {
		cursor: pointer;
		transition: background-color 0.2s ease-in-out;
	}

	.clickable-row:hover {
		background-color: #f0f0f0;
	}

</style>
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
				console.log(transaction.FirstParties)
				console.log(transaction.SecondParties)
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
		
			<!-- Transaction Type -->
			<div class="field">
				<label for="transaction-type">Transaction Type:</label>
				<input id="transaction-type" class="input" type="text" bind:value={transaction.TransactionType} placeholder="Enter transaction type" />
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
		
			<!-- Total Price -->
			<div class="field">
				<label for="total-price">Total Price:</label>
				<input id="total-price" class="input" type="number" step="0.01" bind:value={transaction.TotalPrice} placeholder="Enter total price" />
			</div>
		
			<!-- Act -->
			<div class="field">
				<label for="act">Act:</label>
				<input id="act" class="input" type="text" bind:value={transaction.Act} placeholder="Enter act number or description" />
			</div>
		
			<!-- Page -->
			<div class="field">
				<label for="page">Page:</label>
				<input id="page" class="input" type="number" bind:value={transaction.Page} placeholder="Enter page number" />
			</div>
		
			<!-- Volume -->
			<div class="field">
				<label for="volume">Volume:</label>
				<input id="volume" class="input" type="number" bind:value={transaction.Volume} placeholder="Enter volume number" />
			</div>
		
			<!-- URL -->
			<!-- URL Input Field -->
			<div class="field">
				<label for="url">URL:</label>
				<input id="url" class="input" type="text" bind:value={transaction.URL} placeholder="Enter URL" />
			</div>

			<!-- Read-Only Clickable Link (updates dynamically) -->
			{#if transaction.URL}
				<div class="field">
					<p>
						<a href="{transaction.URL}" target="_blank" rel="noopener noreferrer">
							{transaction.URL}
						</a>
					</p>
				</div>
			{/if}

		
			<!-- Transcriber -->
			<div class="field">
				<label for="transcriber">Transcriber:</label>
				<input id="transcriber" class="input" type="text" bind:value={transaction.Transcriber} placeholder="Enter transcriber's name" />
			</div>
		
			
		
			<!-- Notes Field -->
			<div class="field">
				<label for="notes">Notes:</label>
				<textarea id="notes" class="textarea" bind:value={transaction.Notes} placeholder="Enter additional notes"></textarea>
			</div>

			<h4 class="title is-4">Reviewer ONLY:</h4>
			<!-- isApproved Checkbox -->
			<div class="field">
				<label class="checkbox">
					<input type="checkbox" bind:checked={transaction.isApproved} />
					Approved
				</label>
			</div>
			<!-- Notes Field -->
			<div class="field">
				<label for="DataQuestions">Questions about the Data:</label>
				<textarea id="DataQuestions" class="textarea" bind:value={transaction.DataQuestions} placeholder="Enter your concerns about this data. This won't be visable to the public"></textarea>
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
		<h4 class="title is-4">Enslaved People Associated with This Transaction</h4>
		{#if transactionHumans.length > 0}
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
						<tr on:click={() => window.location.href = `/Humans/ViewHuman.html?HumanId=${human.HumanId}`} class="clickable-row">
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
		{:else}
			<p>No associated enslaved people found for this transaction.</p>
		{/if}


		<!-- Notary Link -->
		<div class="field">
			<h4 class="title is-4">Notary</h4>
			{#if transaction.NotaryHumanId}
				<p>
					<a href="/Human?HumanId={transaction.NotaryHumanId}">
						{transaction.NotaryFirstName} {transaction.NotaryLastName}
					</a>
				</p>
			{:else}
				<p>No Notary Assigned</p>
			{/if}
		</div>

		<!-- First Parties Links -->
		<div class="field">
			<h4 class="title is-4">First Parties</h4>
			<ul>
				{#each transaction.FirstParties as firstParty}
					{#if firstParty.FirstPartyId}
						<li>
							<a href="/Human?HumanId={firstParty.FirstPartyId}">
								{firstParty.FirstPartyFirstName} {firstParty.FirstPartyLastName}
							</a>
						</li>
					{/if}
				{/each}
			</ul>
		</div>

		<!-- Second Parties Links -->
		<div class="field">
			<h4 class="title is-4">Second Parties</h4>
			<ul>
				{#each transaction.SecondParties as secondParty}
					{#if secondParty.SecondPartyId}
						<li>
							<a href="/Human?HumanId={secondParty.SecondPartyId}">
								{secondParty.SecondPartyFirstName} {secondParty.SecondPartyLastName}
							</a>
						</li>
					{/if}
				{/each}
			</ul>
		</div>
	</div>

	


{/if}
