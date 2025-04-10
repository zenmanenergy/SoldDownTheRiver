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
	import { handleGetLocations } from '../Locations/handleGetLocations.js';
	import { handleGetRoles } from '../Roles/handleGetRoles.js';

	import Select from 'svelte-select';
	import moment from 'moment';
	let rawNolaRecords = [];
	let Svelecte; // NEW: variable for Svelecte
	let transaction = {
		date_circa: '',
		date_accuracy: 'D',
		TransactionType: '',
		LocationId: '',
		TotalPrice: '',
		URL: '',
		notes: '',
		DateUpdated:''
	};

	let isLoading = true;
	let transactionId = null;
	let allHumans = [];
	let transactionHumans = [];
	let allLocations = [];
	let allRoles = []; // new variable for roles
	let selectedRoleForHuman = {}; // map human.value --> selected role id

	// New variables for available humans filtering and sorting
	let searchQuery = '';
	let sortColumnSearch = '';
	let sortDirectionSearch = 1;
	$: filteredHumans = allHumans
		.filter(h => 
			((h.FirstName || "").toLowerCase().includes(searchQuery.toLowerCase())) ||
			((h.LastName || "").toLowerCase().includes(searchQuery.toLowerCase())) ||
			(String(h.HumanId || "").toLowerCase().includes(searchQuery.toLowerCase())) ||
			((Array.isArray(h.Roles) ? h.Roles.join(' ').toLowerCase() : String(h.Roles || "").toLowerCase()).includes(searchQuery.toLowerCase())) ||
			((String(h.RacialDescriptor || "").toLowerCase()).includes(searchQuery.toLowerCase()))
		);
	if(sortColumnSearch) {
		filteredHumans.sort((a, b) => {
			let aVal = a[sortColumnSearch] || '';
			let bVal = b[sortColumnSearch] || '';
			// If field is an array, join; otherwise cast to string
			aVal = Array.isArray(aVal) ? aVal.join(' ').toLowerCase() : String(aVal).toLowerCase();
			bVal = Array.isArray(bVal) ? bVal.join(' ').toLowerCase() : String(bVal).toLowerCase();
			return aVal > bVal ? sortDirectionSearch : aVal < bVal ? -sortDirectionSearch : 0;
		});
	}

	// NEW: Pagination variables for available humans
	let currentPageAvailable = 1;
	let itemsPerPageAvailable = 10;
	let totalPagesAvailable = 1;
	$: totalPagesAvailable = Math.max(1, Math.ceil(filteredHumans.length / itemsPerPageAvailable));
	$: displayedAvailableHumans = filteredHumans.slice(
		(currentPageAvailable - 1) * itemsPerPageAvailable,
		currentPageAvailable * itemsPerPageAvailable
	);

	// New function to sort available humans
	function sortAvailableHumans(column) {
		if(sortColumnSearch === column) {
			sortDirectionSearch *= -1;
		} else {
			sortColumnSearch = column;
			sortDirectionSearch = 1;
		}
	}

	function getTransactionIdFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("TransactionId") || null;
	}

	function mapNullToEmpty(obj) {
		return Object.fromEntries(
			Object.entries(obj).map(([key, value]) => [key, value === null ? '' : value])
		);
	}

	let humanCache = []; // Local cache for humans
	let lastFetchTime = null;

// Check if running in the browser before accessing localStorage
if (typeof window !== 'undefined') {
	lastFetchTime = localStorage.getItem('lastFetchTime') || null; // Retrieve from local storage
}

	async function fetchHumans() {
		await handleGetHumans(Session.SessionId, (formattedHumans) => {
			allHumans = formattedHumans;
		});
	}

	onMount(async () => {
		await Session.handleSession();
		const module = await import('svelecte');  // NEW: dynamically import Svelecte
		Svelecte = module.default || module;
		transactionId = getTransactionIdFromURL();

		if (transactionId) {
			// Fetch transaction data
			const data = await handleGetTransaction(Session.SessionId, transactionId);
			if (data) {
				// Map null values to empty strings
				transaction = mapNullToEmpty({ ...data });

				

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
		await fetchHumans();

		// Fetch roles
		await handleGetRoles(Session.SessionId, (data) => {
			if (Array.isArray(data)) {
				allRoles = data; // assume each role object has properties "RoleId" and "Name"
			} else {
				console.error("Error: handleGetRoles did not return an array", data);
				allRoles = [];
			}
		});

		// Fetch locations
		await handleGetLocations(Session.SessionId, (data) => {
			if (Array.isArray(data)) {
				allLocations = data;
			} else {
				console.error("Error: handleGetLocations did not return an array", data);
				allLocations = [];
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

	async function addHumanToTransactionFromAvailable(human) {
		// Changed from human.value to human.HumanId
		const roleId = selectedRoleForHuman[human.HumanId];
		if (!roleId) {
			alert("Please select a role for this human before adding.");
			return;
		}
		await handleSaveTransactionHuman(Session.SessionId, transactionId, human.HumanId, roleId);

		// Refresh transactionHumans after adding a new human
		await handleGetTransactionHumans(Session.SessionId, transactionId, (data) => {
			if (Array.isArray(data)) {
				transactionHumans = data;
			} else {
				console.error("Error: handleGetTransactionHumans did not return an array", data);
				transactionHumans = [];
			}
		});
	}

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
		return date ? new Date(date).toLocaleDateString() : '';
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
		if (!date) return '';
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
		};
		const result = await handleSaveTransaction(Session.SessionId, transactionId, transactionData);
		if (result && result.TransactionId) {
			transactionId = result.TransactionId;
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

	// Predefined order for roles
	const roleOrder = ['Enslaved', 'Notary Public', 'Buyer', 'Seller'];

	// Function to group and sort humans by roleId
	function groupHumansByRole(humans) {
		const grouped = humans.reduce((groups, human) => {
			const roleId = human.RoleId || 'Unassigned'; // Default to 'Unassigned' if RoleId is missing
			if (!groups[roleId]) {
				groups[roleId] = [];
			}
			groups[roleId].push(human);
			return groups;
		}, {});

		// Sort the groups based on the predefined role order
		return Object.keys(grouped)
			.sort((a, b) => {
				const indexA = roleOrder.indexOf(a);
				const indexB = roleOrder.indexOf(b);
				// Roles not in the predefined order will appear last
				return (indexA === -1 ? Infinity : indexA) - (indexB === -1 ? Infinity : indexB);
			})
			.reduce((sortedGroups, sortedKey) => {
				sortedGroups[sortedKey] = grouped[sortedKey];
				return sortedGroups;
			}, {});
	}

	// Reactive statement to group and sort transactionHumans by roleId
	$: groupedHumans = groupHumansByRole(transactionHumans);

	// Function to get the formatted BirthDate based on accuracy
	function calculateBirthDate(human) {
		// If BirthDate exists from the server, use it and format it based on BirthDateAccuracy
		if (human.BirthDate) {
			let birthDate = moment(human.BirthDate);
			if (!birthDate.isValid()) return '';

			// Format based on accuracy
			switch (human.BirthDateAccuracy) {
				case 'D': return birthDate.format('YYYY-MM-DD'); // Full date
				case 'M': return birthDate.format('YYYY-MM');    // Year & month only
				case 'Y': return birthDate.format('YYYY');       // Year only
				default: return '';
			}
		}

		console.log("Calculating BirthDate for:", human);

		// If BirthDate is missing, calculate based on transaction date and age
		if (!transaction.date_circa || (!human.AgeYears && !human.AgeMonths)) {
			return '';
		}

		let baseDate = moment(transaction.date_circa, "YYYY-M-D", true);
		if (!baseDate.isValid()) {
			return '';
		}

		// Subtract Age (years + months) from transaction.date_circa
		let birthDate = baseDate.subtract(human.AgeYears || 0, 'years').subtract(human.AgeMonths || 0, 'months');

		// Format based on accuracy
		switch (human.BirthDateAccuracy) {
			case 'D': return birthDate.format('YYYY-MM-DD');
			case 'M': return birthDate.format('YYYY-MM');
			case 'Y': return birthDate.format('YYYY');
			default: return '';
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
			newHuman.BirthDate = '';
			return;
		}

		let baseDate = moment(transaction.date_circa, "YYYY-M-D", true);
		if (!baseDate.isValid()) {
			newHuman.BirthDate = '';
			return;
		}

		// Subtract Age (years + months) from transaction.date_circa
		let birthDate = baseDate.subtract(newHuman.AgeYears || 0, 'years').subtract(newHuman.AgeMonths || 0, 'months');

		// Format based on accuracy
		switch (newHuman.BirthDateAccuracy) {
			case 'D': newHuman.BirthDate = birthDate.format('YYYY-MM-DD'); break;
			case 'M': newHuman.BirthDate = birthDate.format('YYYY-MM'); break;
			case 'Y': newHuman.BirthDate = birthDate.format('YYYY'); break;
			default: newHuman.BirthDate = '';
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
		<div class="ActionBox">
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
			
				<!-- New Location select box -->
				<div class="field">
					<label for="location">Location:</label>
					<div id="svelecteLocation">
						<svelte:component
							this={Svelecte}
							bind:value={transaction.LocationId}
							options={allLocations.map(loc => ({
								value: loc.LocationId,
								label: loc.Address
							}))}
						/>
					</div>
				</div>
			
				<!-- Total Price -->
				<div class="field">
					<label for="total-price">Total Price:</label>
					<input id="total-price" class="input" type="text" bind:value={transaction.TotalPrice} placeholder="Enter total price" />
				</div>
			
				<!-- Act -->
				<div class="field">
					<label for="act">Act:</label>
					<input id="act" class="input" type="text" bind:value={transaction.Act} placeholder="Enter act number or description" />
				</div>
			
				<!-- Page -->
				<div class="field">
					<label for="page">Page:</label>
					<input id="page" class="input" type="text" bind:value={transaction.Page} placeholder="Enter page number" />
				</div>
			
				<!-- Volume -->
				<div class="field">
					<label for="volume">Volume:</label>
					<input id="volume" class="input" type="text" bind:value={transaction.Volume} placeholder="Enter volume number" />
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

				

				
				


			{#if Object.keys(groupedHumans).length > 0}
				{#each Object.entries(groupedHumans) as [roleId, humans]}
					<h4 class="title is-4">{roleId} People Associated with This Transaction</h4>
					<div class="role-group">
						<table>
							<thead>
								<tr>
									<th width="10%">First Name</th>
									<th width="10%">Last Name</th>
									{#if roleId == "Enslaved"}
										<th>Racial Descriptor</th>
										<th>Sex</th>
										<th>Height (in)</th>
										<th>Physical Features</th>
										<th>Profession</th>
										<th>Birthplace</th>
										<th>Age (Years)</th>
										<th>Age (Months)</th>
										<th>Birthdate</th>
										<th>Price</th>
									{:else}
										<th colspan="10"></th>
									{/if}
									<th width="10%">Action</th>
								</tr>
							</thead>
							<tbody>
								{#each humans as human, index}
										<tr 
											on:click={() => window.open(`/Human?HumanId=${human.HumanId}`, '_blank')} 
											on:keydown={(e) => {
												if (e.key === 'Enter' || e.key === ' ') {
													e.preventDefault();
													window.open(`/Human?HumanId=${human.HumanId}`, '_blank');
												}
											}} 
											class="clickable-row" 
											tabindex="0">
										<td width="10%">{human.FirstName || ''}</td>
										<td width="10%">{human.LastName || ''}</td>
										{#if roleId == "Enslaved"}
											<td>{human.RacialDescriptor || ''}</td>
											<td>{human.Sex || ''}</td>
											<td>{cmToInches(human.Height_cm)}</td>
											<td>{human.physical_features || ''}</td>
											<td>{human.profession || ''}</td>
											<td>{human.BirthPlace || ''}</td>
											<td>{human.AgeYears || ''}</td>
											<td>{human.AgeMonths || ''}</td>
											<td>{calculateBirthDate(human)}</td>
											
											<td>{#if human.Price}${human.Price || ''}{/if}</td>
										{:else}
											<td colspan="10"></td>
										{/if}
										<td width="10%">
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
							</tbody>
						</table>
					</div>
				{/each}
			{:else if transactionId}
				<p>No humans associated with this transaction.</p>
			{/if}
			{#if transactionId}
				<!-- Add button below the list -->
				<div class="add-human-button">
					<button class="button is-primary" on:click={() => window.location.href = `/Human?HumanId=&TransactionId=${transactionId}`}>
						Add a New Human
					</button>
				</div>
				<!-- New Available Humans Table with search, including humanId filter, select box, and add button -->
				<div class="available-humans-table">
					<h4 class="title is-4">Available Humans</h4>
					<!-- Search Box -->
					<div class="field">
						<label for="human-search">Search:</label>
						<input id="human-search" class="input" type="text" placeholder="Search Humans" bind:value={searchQuery} />
					</div>
					<table>
						<thead>
							<tr>
								<th on:click={() => sortAvailableHumans('FirstName')}>
									First Name {sortColumnSearch==='FirstName' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
								</th>
								<th on:click={() => sortAvailableHumans('LastName')}>
									Last Name {sortColumnSearch==='LastName' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
								</th>
								<th on:click={() => sortAvailableHumans('Roles')}>
									Role {sortColumnSearch==='Roles' ? (sortDirectionSearch>0 ? '▲' : '▼') : ''}
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
								<tr>
									<td on:click={() => window.open(`/Human?HumanId=${human.HumanId}`, '_blank')}>
										{human.FirstName}
									</td>
									<td on:click={() => window.open(`/Human?HumanId=${human.HumanId}`, '_blank')}>
										{human.LastName}
									</td>
									<td on:click={() => window.open(`/Human?HumanId=${human.HumanId}`, '_blank')}>
										{Array.isArray(human.Roles) && human.Roles.length > 0 ? human.Roles[0] : ''}
									</td>
									<td on:click={() => window.open(`/Human?HumanId=${human.HumanId}`, '_blank')}>
										{human.RacialDescriptor}
									</td>
									<td>
										<select class="input" bind:value={selectedRoleForHuman[human.HumanId]}>
											<option value="">Select Role</option>
											{#each allRoles as role}
												<option value={role.RoleId}>{role.Role}</option>
											{/each}
										</select>

										
									</td>
									<td>
										<button class="button is-primary is-small" type="button" on:click={() => addHumanToTransactionFromAvailable(human)}>
											Add
										</button>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
					<!-- NEW: Pagination controls for available humans -->
					<div class="pagination">
							<button type="button" on:click={() => currentPageAvailable = Math.max(currentPageAvailable - 1, 1)} disabled={currentPageAvailable === 1}>
								Previous
							</button>
							<span>{currentPageAvailable} / {totalPagesAvailable}</span>
							<button type="button" on:click={() => currentPageAvailable = Math.min(currentPageAvailable + 1, totalPagesAvailable)} disabled={currentPageAvailable === totalPagesAvailable}>
								Next
							</button>
					</div>
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
				{/if}
				<div class="buttons-container">
					<button class="button is-primary" type="submit">Save</button>
					{#if transaction.DateUpdated}
						<span style="margin-left: 1rem;">Last Updated: {transaction.DateUpdated}</span>
					{/if}
					{#if transactionId} 
						<button class="button is-danger delete-button" type="button" on:click={deleteTransaction}>Delete</button>
					{/if}
				</div>
			</form>
			{#if transactionId}
				<br/>
				<h4 class="title is-4">Reference NOLA Records</h4>

				{#if rawNolaRecords.length > 0}
					<table>
						<thead>
							<tr>
								
								<th>Date of Transaction</th>
								<th>Seller</th>
								<th>Buyer</th>
								<th>Type</th>
								<th>Reference URL</th>
							</tr>
						</thead>
						<tbody>
							{#each rawNolaRecords as record}
									<tr 
										style="cursor: pointer;" 
										on:click={() => location.href=`/RawNOLA?NOLA_ID=${encodeURIComponent(record.NOLA_ID)}`} 
										on:keydown={(e) => {
											if (e.key === 'Enter' || e.key === ' ') {
												e.preventDefault();
												location.href=`/RawNOLA?NOLA_ID=${encodeURIComponent(record.NOLA_ID)}`;
											}
										}} 
										tabindex="0">
										<td>
											{moment(record.DateOfTransaction).format('YYYY-MM-DD')}
											
										</td>
									<td>{record.TypeOfTransaction || ''}</td>
									
									<td>{record.FirstParty || ''}</td>
									<td>{record.SecondParty || ''}</td>
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
			
			{/if}
		</div>
	</div>

	


{/if}
