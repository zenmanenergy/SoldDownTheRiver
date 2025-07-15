<!-- src/routes/Reports/Human/+page.svelte -->
<style>
	@import "/static/FormPages.css";
	
	.info-field {
		display: flex;
		margin-bottom: 1rem;
	}
	
	.info-label {
		font-weight: bold;
		min-width: 120px;
		margin-right: 1rem;
	}
	
	.info-value {
		flex: 1;
	}
	
	.human-info {
		background-color: #f8f9fa;
		padding: 1.5rem;
		border-radius: 8px;
		margin-bottom: 2rem;
	}
	
	.report-title {
		color: #363636;
		margin-bottom: 1.5rem;
	}
	
	.section-title {
		color: #363636;
		margin-bottom: 1rem;
		border-bottom: 2px solid #dbdbdb;
		padding-bottom: 0.5rem;
	}
	
	.table-wrapper {
		margin-top: 1rem;
		margin-bottom: 2rem;
	}
	
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

	.aka-list {
		background-color: #f9f9f9;
		padding: 1rem;
		border-radius: 4px;
		margin-bottom: 1rem;
	}

	.aka-item {
		margin-bottom: 0.5rem;
	}

	.transaction-summary {
		border: 1px solid #ccc;
		padding: 15px;
		margin-bottom: 20px;
		background-color: #f9f9f9;
		border-radius: 4px;
	}
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetHuman } from './handleGetHuman.js';
	import { handleGetHumanVoyages } from './handleGetHumanVoyages.js';
	import { handleGetTimelines } from './handleGetTimelines.js';
	import { handleGetAKA } from './handleGetAKA.js';
	import { handleGetTransaction } from './handleGetTransaction.js';
	import { handleGetHumanTransactions } from './handleGetHumanTransactions.js';
	import { handleGetRoles } from './handleGetRoles.js';
	import { handleGetRacialDescriptors } from './handleGetRacialDescriptors.js';

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
		Height_in: '',
		DateUpdated: ''
	};

	let isLoading = true;
	let HumanId = null;
	let voyages = [];
	let timelines = [];
	let akaNames = [];
	let transactionSummary = null;
	let rolesOptions = [];
	let transactions = [];
	let racialDescriptors = [];

	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	function formatDateForDisplay(date, accuracy) {
		if (!date) return "";
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

	function formatDateForInput(date) {
		if (!date) return '';
		const d = new Date(date);
		return d.toISOString().split('T')[0]; // Format as YYYY-MM-DD
	}

	function getAccuracyLabel(accuracy) {
		switch (accuracy) {
			case 'D': return 'Day';
			case 'M': return 'Month';
			case 'Y': return 'Year';
			default: return accuracy;
		}
	}

	function getRoleLabel(roleId) {
		const role = rolesOptions.find(r => r.RoleId === roleId);
		return role ? role.Role : roleId;
	}

	onMount(async () => {
		HumanId = getURLVariable('HumanId') || null;
		const TransactionId = getURLVariable('TransactionId');

		if (HumanId) {
			// Load human data
			const data = await handleGetHuman(HumanId);
			if (data) {
				Human = {
					...data,
					FirstName: data.FirstName || '',
					MiddleName: data.MiddleName || '',
					LastName: data.LastName || '',
					BirthDate: formatDateForInput(data.BirthDate),
					isCompany: data.isCompany || ''
				};

				// Calculate height in inches if cm is available
				if (Human.Height_cm) {
					Human.Height_in = (Human.Height_cm / 2.54).toFixed(2);
				}
			}

			// Load voyages
			voyages = await handleGetHumanVoyages( HumanId) || [];

			// Load timelines
			let _timelines = await handleGetTimelines( HumanId);
			if (_timelines && _timelines.data) {
				timelines = _timelines.data;
			}

			// Load transactions
			const humanTransactions = await handleGetHumanTransactions( HumanId);
			if (humanTransactions) {
				transactions = humanTransactions;
			}

			// Load AKA names
			await handleGetAKA( HumanId, (data) => {
				akaNames = data || [];
			});
		}

		// Load transaction summary if TransactionId is provided
		if (TransactionId) {
			transactionSummary = await handleGetTransaction( TransactionId);
		}

		// Load roles and racial descriptors for display
		rolesOptions = await handleGetRoles() || [];
		racialDescriptors = await handleGetRacialDescriptors() || [];

		isLoading = false;
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}
	<div class="section">
		<h2 class="report-title">Human Report</h2>
		
		{#if Human.HumanId || HumanId}
			{#if transactionSummary}
				<div class="transaction-summary">
					<h3 class="section-title">Transaction Context</h3>
					<div class="info-field">
						<div class="info-label">Transaction:</div>
						<div class="info-value">
							<a target="_blank" href="/Transaction?TransactionId={transactionSummary.TransactionId}">
								View Transaction Details
							</a>
						</div>
					</div>
					<div class="info-field">
						<div class="info-label">Type:</div>
						<div class="info-value">{transactionSummary.TransactionType}</div>
					</div>
					<div class="info-field">
						<div class="info-label">Date:</div>
						<div class="info-value">{formatDate(transactionSummary.date_circa, transactionSummary.date_accuracy)}</div>
					</div>
					{#if transactionSummary.Buyers && transactionSummary.Buyers.length > 0}
						<div class="info-field">
							<div class="info-label">Buyer:</div>
							<div class="info-value">{transactionSummary.Buyers[0].BuyerFirstName || ''} {transactionSummary.Buyers[0].BuyerLastName || ''}</div>
						</div>
					{/if}
					{#if transactionSummary.Sellers && transactionSummary.Sellers.length > 0}
						<div class="info-field">
							<div class="info-label">Seller:</div>
							<div class="info-value">{transactionSummary.Sellers[0].SellerFirstName || ''} {transactionSummary.Sellers[0].SellerLastName || ''}</div>
						</div>
					{/if}
				</div>
			{/if}

			<div class="human-info">
				<h3 class="section-title">
					{Human.isCompany ? 'Company' : 'Person'} Information
				</h3>
				
				{#if Human.isCompany}
					<div class="info-field">
						<div class="info-label">Company Name:</div>
						<div class="info-value">{Human.FirstName}</div>
					</div>
				{:else}
					{#if Human.FirstName}
						<div class="info-field">
							<div class="info-label">First Name:</div>
							<div class="info-value">{Human.FirstName}</div>
						</div>
					{/if}
					
					{#if Human.MiddleName}
						<div class="info-field">
							<div class="info-label">Middle Name:</div>
							<div class="info-value">{Human.MiddleName}</div>
						</div>
					{/if}
					
					{#if Human.LastName}
						<div class="info-field">
							<div class="info-label">Last Name:</div>
							<div class="info-value">{Human.LastName}</div>
						</div>
					{/if}

					{#if Human.BirthDate}
						<div class="info-field">
							<div class="info-label">Birth Date:</div>
							<div class="info-value">
								{formatDateForDisplay(Human.BirthDate, Human.BirthDateAccuracy)}
								<span style="color: #666; font-size: 0.9em;">
									(Accuracy: {getAccuracyLabel(Human.BirthDateAccuracy)})
								</span>
							</div>
						</div>
					{/if}

					{#if Human.RacialDescriptor}
						<div class="info-field">
							<div class="info-label">Racial Descriptor:</div>
							<div class="info-value">{Human.RacialDescriptor}</div>
						</div>
					{/if}

					{#if Human.Sex}
						<div class="info-field">
							<div class="info-label">Sex:</div>
							<div class="info-value">{Human.Sex}</div>
						</div>
					{/if}

					{#if Human.Height_cm || Human.Height_in}
						<div class="info-field">
							<div class="info-label">Height:</div>
							<div class="info-value">
								{#if Human.Height_in}
									{Human.Height_in} inches
								{/if}
								{#if Human.Height_cm}
									({Human.Height_cm} cm)
								{/if}
							</div>
						</div>
					{/if}
				{/if}

				{#if Human.DateUpdated}
					<div class="info-field">
						<div class="info-label">Last Modified:</div>
						<div class="info-value">{moment.utc(Human.DateUpdated).local().format('MMMM Do YYYY, h:mm a')}</div>
					</div>
				{/if}
			</div>

			{#if akaNames.length > 0}
				<div class="table-wrapper">
					<h3 class="section-title">Also Known As (AKA)</h3>
					<div class="aka-list">
						{#each akaNames as aka}
							<div class="aka-item">
								{#if Human.isCompany}
									<strong>{aka.AKAFirstName}</strong>
								{:else}
									<strong>{aka.AKAFirstName} {aka.AKAMiddleName || ''} {aka.AKALastName}</strong>
								{/if}
							</div>
						{/each}
					</div>
				</div>
			{/if}

			{#if timelines.length > 0}
				<div class="table-wrapper">
					<h3 class="section-title">Timeline Events ({timelines.length} records)</h3>
					<table class="table is-fullwidth is-striped">
						<thead>
							<tr>
								<th>Location Type</th>
								<th>Address</th>
								<th>City/State</th>
								<th>Coordinates</th>
								<th>Date</th>
								<th>Role</th>
							</tr>
						</thead>
						<tbody>
							{#each timelines as timeline}
								<tr on:click={() => window.open(`/Admin/Reports/Location?LocationId=${timeline.LocationId}`, '_blank')} style="cursor: pointer;">
									<td>{timeline.LocationType || ''}</td>
									<td>{timeline.Address || ''}</td>
									<td>{timeline.City || ''}{timeline.State ? ', ' + timeline.State : ''}</td>
									<td>{timeline.Latitude || ''},{timeline.Longitude || ''}</td>
									<td>{formatDate(timeline.Date_Circa, timeline.Date_Accuracy)}</td>
									<td>{getRoleLabel(timeline.RoleId)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}

			{#if voyages.length > 0}
				<div class="table-wrapper">
					<h3 class="section-title">Voyages ({voyages.length} records)</h3>
					<table class="table is-fullwidth is-striped">
						<thead>
							<tr>
								<th>Voyage ID</th>
								<th>Role</th>
								<th>Notes</th>
							</tr>
						</thead>
						<tbody>
							{#each voyages as voyage}
								<tr on:click={() => window.open(`/Admin/Voyage?VoyageId=${voyage.VoyageId}`, '_blank')} style="cursor: pointer;">
									<td>{voyage.VoyageId}</td>
									<td>{voyage.RoleId}</td>
									<td>{voyage.Notes || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}

			{#if transactions.length > 0}
				<div class="table-wrapper">
					<h3 class="section-title">Transactions ({transactions.length} records)</h3>
					<table class="table is-fullwidth is-striped">
						<thead>
							<tr>
								<th>Type</th>
								<th>Date</th>
								<th>Notary</th>
								<th>Sellers</th>
								<th>Buyers</th>
							</tr>
						</thead>
						<tbody>
							{#each transactions as txn}
								<tr on:click={() => window.open(`/Admin/Transaction?TransactionId=${txn.TransactionId}`, '_blank')} style="cursor: pointer;">
									<td>{txn.TransactionType || ''}</td>
									<td>{formatDate(txn.date_circa, txn.date_accuracy)}</td>
									<td>{txn.Notary || ''}</td>
									<td>{txn.Sellers || ''}</td>
									<td>{txn.Buyers || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}

			{#if !timelines.length && !voyages.length && !transactions.length && !akaNames.length}
				<div class="notification is-info">
					No additional records found for this person.
				</div>
			{/if}

		{:else}
			<div class="notification is-warning">
				No Human ID provided. Please provide a HumanId parameter in the URL.
			</div>
		{/if}
	</div>
{/if}
