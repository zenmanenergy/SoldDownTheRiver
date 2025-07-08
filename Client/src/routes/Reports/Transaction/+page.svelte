<!-- src/routes/Reports/Transaction/+page.svelte -->
<!-- Read-only Transaction Report View -->

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { Session } from '../../Session.js';
	import { handleGetTransaction } from '../../Transaction/handleGetTransaction.js';
	import { handleGetTransactionHumans } from '../../Transaction/handleGetTransactionHumans.js';
	import { handleGetRawNolas } from '../../Transaction/handleGetRawNolas.js';
	import { handleGetLocations } from '../../Locations/handleGetLocations.js';
	import { handleGetRoles } from '../../Roles/handleGetRoles.js';
	import { handleGetLinkReferences } from '../../References/handleGetLinkReferences.js';

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
		await Session.handleSession();
		transactionId = getTransactionIdFromURL();

		if (!transactionId) {
			console.error("No TransactionId provided");
			isLoading = false;
			return;
		}

		// Fetch transaction data
		const data = await handleGetTransaction(Session.SessionId, transactionId);
		if (data) {
			transaction = mapNullToEmpty({ ...data });

			// Convert date format
			if (transaction.date_circa) {
				const parsedDate = moment.utc(transaction.date_circa, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);
				if (parsedDate.isValid()) {
					transaction.date_circa = parsedDate.format("YYYY-MM-DD");
				}
			}

			// Fetch NOLA records if available
			if (transaction.NOLA_ID) {
				await handleGetRawNolas(Session.SessionId, [transaction.NOLA_ID], (records) => {
					rawNolaRecords = records;
				});
			}
		}

		// Fetch related data
		await Promise.all([
			// Fetch roles
			handleGetRoles(Session.SessionId, (data) => {
				allRoles = Array.isArray(data) ? data : [];
			}),
			// Fetch locations
			handleGetLocations(Session.SessionId, (data) => {
				allLocations = Array.isArray(data) ? data : [];
			}),
			// Fetch humans associated with this transaction
			handleGetTransactionHumans(Session.SessionId, transactionId, (data) => {
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
								<td><strong>Transaction ID:</strong></td>
								<td>{transaction.TransactionId || transactionId}</td>
							</tr>
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
						</tbody>
					</table>
				</div>
				<div class="column is-half">
					<table class="table is-borderless">
						<tbody>
							<tr>
								<td><strong>Total Price:</strong></td>
								<td>{transaction.TotalPrice ? `$${transaction.TotalPrice}` : "N/A"}</td>
							</tr>
							<tr>
								<td><strong>Act:</strong></td>
								<td>{transaction.Act || "N/A"}</td>
							</tr>
							<tr>
								<td><strong>Page:</strong></td>
								<td>{transaction.Page || "N/A"}</td>
							</tr>
							<tr>
								<td><strong>Volume:</strong></td>
								<td>{transaction.Volume || "N/A"}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			{#if transaction.URL}
				<div class="field">
					<label class="label">Source URL:</label>
					<div class="content">
						<a href={transaction.URL} target="_blank" rel="noopener noreferrer">
							{transaction.URL}
						</a>
					</div>
				</div>
			{/if}

			{#if transaction.Transcriber}
				<div class="field">
					<label class="label">Transcriber:</label>
					<div class="content">
						<p>{transaction.Transcriber}</p>
					</div>
				</div>
			{/if}

			{#if transaction.Notes}
				<div class="field">
					<label class="label">Notes:</label>
					<div class="content">
						<p>{transaction.Notes}</p>
					</div>
				</div>
			{/if}

			{#if transaction.isApproved !== null}
				<div class="field">
					<label class="label">Status:</label>
					<div class="content">
						<span class="tag {transaction.isApproved ? 'is-success' : 'is-warning'}">
							{transaction.isApproved ? 'Approved' : 'Pending Review'}
						</span>
					</div>
				</div>
			{/if}

			{#if transaction.DateUpdated}
				<div class="field">
					<label class="label">Last Updated:</label>
					<div class="content">
						<p>{moment.utc(transaction.DateUpdated).local().format('MMMM Do YYYY, h:mm a')}</p>
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
							<tr on:click={() => window.location.href = `/RawNOLA?NOLA_ID=${encodeURIComponent(record.NOLA_ID)}`} style="cursor:pointer;">
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

<style>
	.loading-screen {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 50vh;
	}

	.spinner {
		border: 4px solid #f3f3f3;
		border-top: 4px solid #3498db;
		border-radius: 50%;
		width: 40px;
		height: 40px;
		animation: spin 2s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.title-container {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.ActionBox {
		background-color: #f8f9fa;
		border: 1px solid #e9ecef;
		border-radius: 8px;
		padding: 1.5rem;
		margin-bottom: 1.5rem;
	}

	.table-container {
		overflow-x: auto;
	}

	tr:hover {
		background-color: #f5f5f5;
	}

	.table.is-borderless td {
		border: none;
		padding: 0.5rem 0.75rem;
	}

	.table.is-borderless tbody tr:last-child td {
		border-bottom: none;
	}

	.box {
		margin-bottom: 0;
	}

	.tag.is-info {
		background-color: #3298dc;
		color: white;
		font-weight: 500;
	}

	.tag.is-success {
		background-color: #48c774;
		color: white;
		font-weight: 500;
	}

	.tag.is-warning {
		background-color: #ffdd57;
		color: rgba(0, 0, 0, 0.7);
		font-weight: 500;
	}

	.notification.is-info {
		margin-top: 1rem;
		text-align: center;
	}

	.notification.is-warning {
		margin-top: 1rem;
	}

	a {
		color: #3273dc;
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}
</style>
