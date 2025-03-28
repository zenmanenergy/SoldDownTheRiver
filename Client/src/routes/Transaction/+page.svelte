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
	import { handleSaveTransactionHuman } from './handleSaveTransactionHuman.js';
	import { handleDeleteTransactionHuman } from './handleDeleteTransactionHuman.js';
	import { handleGetRawNolas } from './handleGetRawNolas.js';

	import Select from 'svelte-select';
	import moment from 'moment';
	let rawNolaRecords = [];
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

	function mapNullToEmpty(obj) {
		return Object.fromEntries(
			Object.entries(obj).map(([key, value]) => [key, value === null ? '' : value])
		);
	}

	onMount(async () => {
		await Session.handleSession();
		transactionId = getTransactionIdFromURL();

		if (transactionId) {
			// Fetch transaction data
			const data = await handleGetTransaction(Session.SessionId, transactionId);
			if (data) {
				// Map null values to empty strings
				transaction = mapNullToEmpty({ ...data });

				// Ensure FirstParties and SecondParties are valid arrays
				transaction.FirstParties = transaction.FirstParties || [];
				transaction.SecondParties = transaction.SecondParties || [];

				// Convert date format
				if (transaction.date_circa) {
					const parsedDate = moment.utc(transaction.date_circa, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);
					if (parsedDate.isValid()) {
						transaction.date_circa = parsedDate.format("YYYY-MM-DD");
					}
				}

				// Ensure transaction has NOLA_ID
				if (transaction.NOLA_ID) {
					await handleGetRawNolas(Session.SessionId, [transaction.NOLA_ID], (records) => {
						rawNolaRecords = records;
					});
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

	function toggleSort(column) {
		if (sortColumn === column) {
			sortDirection *= -1; // Reverse direction if already sorting by this column
		} else {
			sortColumn = column;
			sortDirection = 1;
		}

		filteredRecords = [...rawNolaRecords].sort((a, b) => {
			let valA = a[column] || '';
			let valB = b[column] || '';

			// Convert dates to timestamps for sorting
			if (column === 'DateOfTransaction') {
				valA = new Date(valA).getTime();
				valB = new Date(valB).getTime();
			}

			// Handle string and numeric sorting
			if (typeof valA === 'string') valA = valA.toLowerCase();
			if (typeof valB === 'string') valB = valB.toLowerCase();

			return valA > valB ? sortDirection : valA < valB ? -sortDirection : 0;
		});
	}

	function formatDateOfTransaction(date) {
		return date ? new Date(date).toLocaleDateString() : 'N/A';
	}
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
		return cm ? (cm / 2.54).toFixed(2) : '';
	}

	// Helper function to format birthdate based on accuracy
	function formatBirthDate(date, accuracy) {
		console.log("date",date)
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
			NotaryHumanId: selectedNotary?.value || null, // Ensure NotaryHumanId is set
			FirstParties: JSON.stringify(selectedFirstParty.map(fp => ({ FirstPartyId: fp.value }))), // Convert to JSON string
			SecondParties: JSON.stringify(selectedSecondParty.map(sp => ({ SecondPartyId: sp.value }))), // Convert to JSON string
		};

		const success = await handleSaveTransaction(Session.SessionId, transactionId, transactionData);
		if (success) {
			window.location.href = `/Transaction?TransactionId=${transactionId}`;
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

	let newHuman = {
		FirstName: '',
		LastName: '',
		RacialDescriptor: '',
		Sex: '',
		Height_cm: '',
		physical_features: '',
		profession: '',
		BirthPlace: '',
		AgeYears: '',
		AgeMonths: '',
		BirthDateAccuracy: 'D',
		BirthDate: '',
		Price: '', // NEW FIELD FOR PRICE
	};

	

	

	// Function to get the formatted BirthDate based on accuracy
	function calculateBirthDate(human) {
		// If BirthDate exists from the server, use it and format it based on BirthDateAccuracy
		if (human.BirthDate) {
			let birthDate = moment(human.BirthDate);
			if (!birthDate.isValid()) return 'N/A';

			// Format based on accuracy
			switch (human.BirthDateAccuracy) {
				case 'D': return birthDate.format('YYYY-MM-DD'); // Full date
				case 'M': return birthDate.format('YYYY-MM');    // Year & month only
				case 'Y': return birthDate.format('YYYY');       // Year only
				default: return 'N/A';
			}
		}

		console.log("Calculating BirthDate for:", human);

		// If BirthDate is missing, calculate based on transaction date and age
		if (!transaction.date_circa || (!human.AgeYears && !human.AgeMonths)) {
			return 'N/A';
		}

		let baseDate = moment(transaction.date_circa, "YYYY-M-D", true);
		if (!baseDate.isValid()) {
			return 'N/A';
		}

		// Subtract Age (years + months) from transaction.date_circa
		let birthDate = baseDate.subtract(human.AgeYears || 0, 'years').subtract(human.AgeMonths || 0, 'months');

		// Format based on accuracy
		switch (human.BirthDateAccuracy) {
			case 'D': return birthDate.format('YYYY-MM-DD');
			case 'M': return birthDate.format('YYYY-MM');
			case 'Y': return birthDate.format('YYYY');
			default: return 'N/A';
		}
	}


	async function addHumanToTransaction() {
		

		// Set HumanId to blank so the server can generate one
		newHuman.HumanId = "";

		// Calculate Birthdate before saving
		newHuman.BirthDate = calculateBirthDate(newHuman);

		try {
			// Save the human to the database and get the response
			const savedHuman = await handleSaveTransactionHuman(Session.SessionId, transactionId, newHuman);

			// Append the server response to transactionHumans
			transactionHumans = [...transactionHumans, savedHuman];

			// Reset input fields
			newHuman = {
				FirstName: '',
				LastName: '',
				RacialDescriptor: '',
				Sex: '',
				Height_cm: '',
				physical_features: '',
				profession: '',
				BirthPlace: '',
				AgeYears: '',
				AgeMonths: '',
				BirthDateAccuracy: 'D',
				BirthDate: '',
				Price: '',
				Notes: '',
			};
		} catch (error) {
			console.error("Error saving human:", error);
			alert("Failed to save human.");
		}
	}




	// Function to remove a human from the list
	function removeHumanFromTransaction(index, event) {
		event.stopPropagation(); // Prevent row click redirect
		transactionHumans = transactionHumans.filter((_, i) => i !== index);
	}
	

	// Reactive `$:` statement to update BirthDate immediately when Age changes
	$: {
		if (newHuman.AgeYears !== '' || newHuman.AgeMonths !== '' || transaction.date_circa) {
			updateNewHumanBirthDate();
		}
	}

	// Function to calculate Birthdate based on Age (years + months)
	function updateNewHumanBirthDate() {
		if (!transaction.date_circa || (!newHuman.AgeYears && !newHuman.AgeMonths)) {
			newHuman.BirthDate = 'N/A';
			return;
		}

		let baseDate = moment(transaction.date_circa, "YYYY-M-D", true);
		if (!baseDate.isValid()) {
			newHuman.BirthDate = 'N/A';
			return;
		}

		// Subtract Age (years + months) from transaction.date_circa
		let birthDate = baseDate.subtract(newHuman.AgeYears || 0, 'years').subtract(newHuman.AgeMonths || 0, 'months');

		// Format based on accuracy
		switch (newHuman.BirthDateAccuracy) {
			case 'D': newHuman.BirthDate = birthDate.format('YYYY-MM-DD'); break;
			case 'M': newHuman.BirthDate = birthDate.format('YYYY-MM'); break;
			case 'Y': newHuman.BirthDate = birthDate.format('YYYY'); break;
			default: newHuman.BirthDate = 'N/A';
		}
	}


	// Ensure Birthdate updates when Age or Date changes
	$: updateNewHumanBirthDate();


</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<h3 class="title is-2">{transactionId ? 'Edit' : 'Add'} Transaction</h3>
		
		<form on:submit|preventDefault={submitTransaction}>
			<!-- Transaction Date -->
			<div class="field">
				<label for="date">Date:</label>
				<input id="date" class="input" type="date" bind:value={transaction.date_circa} on:input={updateDateFormat} />
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
						<Select 
							id="notary" 
							bind:value={selectedNotary} 
							items={allHumans} 
							on:change={() => transaction.NotaryHumanId = selectedNotary?.value || null} 
						/>
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
		

		<h4 class="title is-4">Enslaved People Associated with This Transaction</h4>

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
					<th>Age (Years)</th>
					<th>Age (Months)</th>
					<th>Birthdate</th>
					<th>BirthDateAccuracy</th>
					<th>Price</th> <!-- NEW COLUMN -->
					<th>Action</th>
				</tr>
			</thead>
			<tbody>
				<!-- Existing Humans -->
				{#each transactionHumans as human, index}
					<tr on:click={() => window.location.href = `/Human?HumanId=${human.HumanId}`} class="clickable-row">
						<td>{human.FirstName || ''}</td>
						<td>{human.LastName || ''}</td>
						<td>{human.RacialDescriptor || ''}</td>
						<td>{human.Sex || ''}</td>
						<td>{cmToInches(human.Height_cm)}</td>
						<td>{human.physical_features || ''}</td>
						<td>{human.profession || ''}</td>
						<td>{human.BirthPlace || ''}</td>
						<td>{human.AgeYears || ''}</td>
						<td>{human.AgeMonths || ''}</td>
						<td>{calculateBirthDate(human)}</td>
						<td>
							{#if human.BirthDateAccuracy === 'D'}
								Day
							{:else if human.BirthDateAccuracy === 'M'}
								Month
							{:else if human.BirthDateAccuracy === 'Y'}
								Year
							{:else}
								Unknown
							{/if}
						</td>
						<td>${human.Price || ''}</td> <!-- NEW PRICE COLUMN -->
						<td>
							<button class="button is-danger is-small" 
								type="button" 
								on:click={e => {
									e.stopPropagation(); // Prevent row click redirect
									handleDeleteTransactionHuman(Session.SessionId, transactionId, human.HumanId);
								}}>
								Remove
							</button>
						</td>
						
					</tr>
				{/each}

				<!-- Row for Adding a New Human -->
				<tr>
					<td><input type="text" class="input" bind:value={newHuman.FirstName} placeholder="First Name" /></td>
					<td><input type="text" class="input" bind:value={newHuman.LastName} placeholder="Last Name" /></td>
					<td><input type="text" class="input" bind:value={newHuman.RacialDescriptor} placeholder="Racial Descriptor" /></td>
					<td><input type="text" class="input" bind:value={newHuman.Sex} placeholder="Sex" /></td>
					<td><input type="number" class="input" bind:value={newHuman.Height_cm} placeholder="Height (cm)" /></td>
					<td><input type="text" class="input" bind:value={newHuman.physical_features} placeholder="Physical Features" /></td>
					<td><input type="text" class="input" bind:value={newHuman.profession} placeholder="Profession" /></td>
					<td><input type="text" class="input" bind:value={newHuman.BirthPlace} placeholder="Birthplace" /></td>
					<td><input type="number" class="input" bind:value={newHuman.AgeYears} placeholder="Age (Years)" /></td>
					<td><input type="number" class="input" bind:value={newHuman.AgeMonths} placeholder="Age (Months)" /></td>
					<td><input type="text" class="input" readonly bind:value={newHuman.BirthDate} /></td>
					<td>
						<select class="input" bind:value={newHuman.BirthDateAccuracy}>
							<option value="D">Day</option>
							<option value="M">Month</option>
							<option value="Y">Year</option>
						</select>
					</td>
					<td><input type="number" class="input" bind:value={newHuman.Price} placeholder="Price (USD)" step="0.01" /></td> <!-- NEW PRICE FIELD -->
					<td>
						<button class="button is-primary is-small" type="button" on:click={addHumanToTransaction}>Add</button>
					</td>
				</tr>
			</tbody>
		</table>



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

		<h4 class="title is-4">NOLA Records</h4>

		{#if rawNolaRecords.length > 0}
			<table>
				<thead>
					<tr>
						
						<th>First Party</th>
						<th>Second Party</th>
						<th>Type</th>
						<th>Date of Transaction</th>
						<th>Reference URL</th>
					</tr>
				</thead>
				<tbody>
					{#each rawNolaRecords as record}
						<tr style="cursor: pointer;" on:click={() => location.href=`/RawNola?NOLA_ID=${encodeURIComponent(record.NOLA_ID)}`} >
							<td>{record.DateOfTransaction ? new Date(record.DateOfTransaction).toLocaleDateString() : 'N/A'}</td>
							<td>{record.TypeOfTransaction || 'N/A'}</td>
							
							<td>{record.FirstParty || 'N/A'}</td>
							<td>{record.SecondParty || 'N/A'}</td>
							<td>
								{#if record.ReferenceURL}
									<a href={record.ReferenceURL} target="_blank">View</a>
								{/if}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{:else}
			<p>No associated NOLA records found.</p>
		{/if}


	</div>

	


{/if}
