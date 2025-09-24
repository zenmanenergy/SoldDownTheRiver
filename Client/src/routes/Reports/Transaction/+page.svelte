<!-- src/routes/Reports/Transaction/+page.svelte -->
<!-- Read-only Transaction Report View -->

<style>
	@import "/static/FormPages.css";
	
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetTransaction } from './handleGetTransaction.js';
	import { handleGetTransactionHumans } from './handleGetTransactionHumans.js';
	import { handleGetLocations } from './handleGetLocations.js';
	import { handleGetRoles } from './handleGetRoles.js';
	import { handleGetLinkReferences } from './handleGetLinkReferences.js';

	let transaction = {
		TransactionId: '',
		date_circa: '',
		date_accuracy: 'D',
		TransactionType: '',
		LocationId: '',
		TotalPrice: '',
		Act: '',
		Page: '',
		Volume: '',
		URL: '',
		Transcriber: '',
		Notes: '',
		isApproved: false,
		DataQuestions: '',
		DateUpdated: ''
	};

	let isLoading = true;
	let transactionId = null;
	let transactionHumans = [];
	let allLocations = [];
	let allRoles = [];
	let rawNolaRecords = [];
	let transactionReferences = [];
	let isReferencesLoading = true;

	// Predefined order for roles
	const roleOrder = ['Enslaved', 'Notary Public', 'Buyer', 'Seller'];

	function getTransactionIdFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("TransactionId") || null;
	}

	function mapNullToEmpty(obj) {
		return Object.fromEntries(
			Object.entries(obj).map(([key, value]) => [key, value === null ? '' : value])
		);
	}

	// Function to group and sort humans by roleId
	function groupHumansByRole(humans) {
		const grouped = humans.reduce((groups, human) => {
			const roleId = human.RoleId || 'Unassigned';
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
		if (human.BirthDate) {
			let birthDate = moment(human.BirthDate);
			if (!birthDate.isValid()) return '';

			switch (human.BirthDateAccuracy) {
				case 'D': return birthDate.format('YYYY-MM-DD');
				case 'M': return birthDate.format('YYYY-MM');
				case 'Y': return birthDate.format('YYYY');
				default: return '';
			}
		}

		if (!transaction.date_circa || (!human.AgeYears && !human.AgeMonths)) {
			return '';
		}

		let baseDate = moment(transaction.date_circa, "YYYY-M-D", true);
		if (!baseDate.isValid()) {
			return '';
		}

		let birthDate = baseDate.subtract(human.AgeYears || 0, 'years').subtract(human.AgeMonths || 0, 'months');

		switch (human.BirthDateAccuracy) {
			case 'D': return birthDate.format('YYYY-MM-DD');
			case 'M': return birthDate.format('YYYY-MM');
			case 'Y': return birthDate.format('YYYY');
			default: return '';
		}
	}

	// Helper function to convert centimeters to inches
	function cmToInches(cm) {
		return cm ? (cm / 2.54).toFixed(2) : '';
	}

	// Format displayed date based on accuracy
	function getFormattedDate() {
		if (!transaction.date_circa) return "";
		const parts = transaction.date_circa.split("-");
		switch (transaction.date_accuracy) {
			case "D": return moment(transaction.date_circa).format('MMMM D, YYYY');
			case "M": return moment(`${parts[0]}-${parts[1]}-01`).format('MMMM YYYY');
			case "Y": return `${parts[0]}`;
			default: return moment(transaction.date_circa).format('MMMM D, YYYY');
		}
	}

	function getLocationName() {
		if (!transaction.LocationId) return "Unknown";
		const location = allLocations.find(l => l.LocationId === transaction.LocationId);
		return location ? location.Address : "Unknown";
	}

	function getAccuracyLabel(accuracy) {
		switch (accuracy) {
			case 'D': return 'Day';
			case 'M': return 'Month';
			case 'Y': return 'Year';
			default: return accuracy;
		}
	}

	async function setTransactionReferences(data) {
		transactionReferences = data;
	}

	onMount(async () => {
		transactionId = getTransactionIdFromURL();

		if (!transactionId) {
			console.error("No TransactionId provided");
			isLoading = false;
			return;
		}

		// Fetch transaction data
		const data = await handleGetTransaction(transactionId);
		if (data) {
			transaction = mapNullToEmpty({ ...data });

			// Convert date format
			if (transaction.date_circa) {
				const parsedDate = moment.utc(transaction.date_circa, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);
				if (parsedDate.isValid()) {
					transaction.date_circa = parsedDate.format("YYYY-MM-DD");
				}
			}

			
		}

		// Fetch related data
		await Promise.all([
			// Fetch roles
			handleGetRoles((data) => {
				allRoles = Array.isArray(data) ? data : [];
			}),
			// Fetch locations
			handleGetLocations( (data) => {
				allLocations = Array.isArray(data) ? data : [];
			}),
			// Fetch humans associated with this transaction
			handleGetTransactionHumans(transactionId, (data) => {
				transactionHumans = Array.isArray(data) ? data : [];
			})
		]);

		// Fetch references linked to this transaction
		await handleGetLinkReferences(transactionId, 'transaction', setTransactionReferences);
		isReferencesLoading = false;

		isLoading = false;
	});
</script>

<svelte:head>
	<title>Transaction Report - {transaction.TransactionType}</title>
</svelte:head>

{#if isLoading}
<div class="loading-screen">
	<div class="spinner"></div>
</div>
{:else}

<div class="section">
	<div class="ActionBox">
		<div class="title-container">
			<h3 class="title is-2">Transaction Report</h3>
		</div>

		<!-- Transaction Information -->
		<div class="content">
			<div class="columns">
				<div class="column is-half">
					<table class="table is-borderless">
						<tbody>
							
							<tr>
								<td><strong>Date:</strong></td>
								<td>
									{getFormattedDate()}
									{#if transaction.date_accuracy !== 'D'}
										<span class="tag is-info is-small">
											{getAccuracyLabel(transaction.date_accuracy)} precision
										</span>
									{/if}
								</td>
							</tr>
							<tr>
								<td><strong>Transaction Type:</strong></td>
								<td>{transaction.TransactionType || "N/A"}</td>
							</tr>
							<tr>
								<td><strong>Location:</strong></td>
								<td>
									{#if transaction.LocationId}
										<a href="/Reports/Location?LocationId={transaction.LocationId}" target="_blank">
											{getLocationName()}
										</a>
									{:else}
										N/A
									{/if}
								</td>
							</tr>
							<tr>
								<td><strong>Total Price:</strong></td>
								<td>{transaction.TotalPrice ? `$${transaction.TotalPrice}` : "N/A"}</td>
							</tr>
						</tbody>
					</table>
				</div>
				
			</div>

			

			

			{#if transaction.Notes}
				<div class="field">
					<label class="label">Notes:</label>
					<div class="content">
						<p>{transaction.Notes}</p>
					</div>
				</div>
			{/if}

			
		</div>
	</div>

	<!-- People Associated with Transaction -->
	{#if Object.keys(groupedHumans).length > 0}
		{#each Object.entries(groupedHumans) as [roleId, humans]}
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-4">{roleId} ({humans.length})</h3>
				</div>
				
				<div class="table-container">
					<table class="table is-striped is-hoverable is-fullwidth">
						<thead>
							<tr>
								<th>First Name</th>
								<th>Last Name</th>
								{#if roleId === "Enslaved"}
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
								{/if}
							</tr>
						</thead>
						<tbody>
							{#each humans as human}
								<tr on:click={() => window.location.href = `/Reports/Human?HumanId=${human.HumanId}`} style="cursor:pointer;">
									<td>{human.FirstName || ''}</td>
									<td>{human.LastName || ''}</td>
									{#if roleId === "Enslaved"}
										<td>{human.RacialDescriptor || ''}</td>
										<td>{human.Sex || ''}</td>
										<td>{cmToInches(human.Height_cm) || ''}</td>
										<td>{human.physical_features || ''}</td>
										<td>{human.profession || ''}</td>
										<td>{human.BirthPlace || ''}</td>
										<td>{human.AgeYears || ''}</td>
										<td>{human.AgeMonths || ''}</td>
										<td>{calculateBirthDate(human)}</td>
										<td>{human.Price ? `$${human.Price}` : ''}</td>
									{/if}
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/each}
	{:else}
		<div class="ActionBox">
			<div class="content">
				<p>No people associated with this transaction.</p>
			</div>
		</div>
	{/if}

	<!-- Transaction Statistics -->
	<div class="ActionBox">
		<div class="title-container">
			<h3 class="title is-4">Transaction Statistics</h3>
		</div>
		
		<div class="columns">
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-danger">
						{groupedHumans['Enslaved'] ? groupedHumans['Enslaved'].length : 0}
					</p>
					<p class="subtitle">Enslaved People</p>
				</div>
			</div>
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-info">
						{groupedHumans['Buyer'] ? groupedHumans['Buyer'].length : 0}
					</p>
					<p class="subtitle">Buyer(s)</p>
				</div>
			</div>
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-warning">
						{groupedHumans['Seller'] ? groupedHumans['Seller'].length : 0}
					</p>
					<p class="subtitle">Seller(s)</p>
				</div>
			</div>
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-success">
						{groupedHumans['Notary Public'] ? groupedHumans['Notary Public'].length : 0}
					</p>
					<p class="subtitle">Notary</p>
				</div>
			</div>
		</div>

		{#if transaction.TotalPrice}
			{@const enslavedCount = groupedHumans['Enslaved'] ? groupedHumans['Enslaved'].length : 0}
			{#if enslavedCount > 0}
				{@const averagePrice = (parseFloat(transaction.TotalPrice) / enslavedCount).toFixed(2)}
				<div class="notification is-info">
					<strong>Average Price per Enslaved Person:</strong> ${averagePrice}
					<br><strong>Total Transaction Value:</strong> ${transaction.TotalPrice}
				</div>
			{/if}
		{/if}
	</div>

	<!-- NOLA Records Section -->
	{#if rawNolaRecords.length > 0}
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-4">Reference NOLA Records ({rawNolaRecords.length})</h3>
			</div>
			
			<div class="table-container">
				<table class="table is-striped is-hoverable is-fullwidth">
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
							<tr>
								<td>{moment.utc(record.DateOfTransaction).format('YYYY-MM-DD')}</td>
								<td>{record.FirstParty || ''}</td>
								<td>{record.SecondParty || ''}</td>
								<td>{record.TypeOfTransaction || ''}</td>
								<td>
									{#if record.ReferenceURL}
										<a href={record.ReferenceURL} target="_blank" rel="noopener noreferrer" on:click|stopPropagation>
											View
										</a>
									{:else}
										N/A
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{/if}

	<!-- References Section -->
	{#if transactionId}
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-4">References ({transactionReferences.length})</h3>
			</div>
			{#if isReferencesLoading}
				<div>Loading references...</div>
			{:else if transactionReferences.length === 0}
				<div class="content">
					<p>No references linked to this transaction.</p>
				</div>
			{:else}
				<div class="table-container">
					<table class="table is-striped is-hoverable is-fullwidth">
						<thead>
							<tr>
								<th>URL</th>
								<th>Notes</th>
								<th>Date Updated</th>
							</tr>
						</thead>
						<tbody>
							{#each transactionReferences as reference}
								<tr on:click={() => window.location.href = `/Reports/Reference?ReferenceId=${reference.ReferenceId}`} style="cursor:pointer;">
									<td>
										<a href={reference.URL} target="_blank" rel="noopener noreferrer" on:click|stopPropagation>
											{reference.URL}
										</a>
									</td>
									<td>{reference.Notes || "N/A"}</td>
									<td>{reference.dateUpdated ? moment.utc(reference.dateUpdated).format('MMMM D, YYYY') : "N/A"}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Data Quality Section -->
	{#if transaction.DataQuestions}
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-4">Data Quality Notes</h3>
			</div>
			<div class="content">
				<div class="notification is-warning">
					<strong>Reviewer Notes:</strong>
					<p>{transaction.DataQuestions}</p>
				</div>
			</div>
		</div>
	{/if}
</div>
{/if}
