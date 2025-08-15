<!-- src/routes/Reports/Human/+page.svelte -->


<style>
	@import "/static/FormPages.css";
	
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
	import { handleGetCombinedTimeline } from './handleGetCombinedTimeline.js';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';

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
	let combinedTimeline = [];
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

	function handleCombinedTimelineClick(event) {
		const anchor = event.target.closest('a');
		if (anchor && anchor.getAttribute('href') && anchor.getAttribute('href').startsWith('/Reports/Human')) {
			event.preventDefault();
			goto(anchor.getAttribute('href'));
		}
	}

	// Move the data loading logic into a function
	async function loadHumanPageData(HumanId, TransactionId) {
		isLoading = true;

		if (HumanId) {
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

				// Set FirstName to "Unnamed" if all name fields are empty
				if (!Human.FirstName && !Human.MiddleName && !Human.LastName) {
					Human.FirstName = "Unnamed";
				}

				if (Human.Height_cm) {
					Human.Height_in = (Human.Height_cm / 2.54).toFixed(2);
				}
			}

			voyages = await handleGetHumanVoyages(HumanId) || [];

			let _timelines = await handleGetTimelines(HumanId);
			if (_timelines && _timelines.data) {
				timelines = _timelines.data;
			}

			combinedTimeline = await handleGetCombinedTimeline(HumanId) || [];

			const humanTransactions = await handleGetHumanTransactions(HumanId);
			if (humanTransactions) {
				transactions = humanTransactions;
			}

			await handleGetAKA(HumanId, (data) => {
				akaNames = data || [];
			});
		}

		if (TransactionId) {
			transactionSummary = await handleGetTransaction(TransactionId);
		}

		rolesOptions = await handleGetRoles() || [];
		racialDescriptors = await handleGetRacialDescriptors() || [];

		isLoading = false;
	}

	// Reactively reload data when HumanId changes in the URL
	$: {
		const currentHumanId = $page.url.searchParams.get('HumanId');
		const currentTransactionId = $page.url.searchParams.get('TransactionId');
		if (currentHumanId !== HumanId) {
			HumanId = currentHumanId;
			loadHumanPageData(HumanId, currentTransactionId);
		}
	}

	onMount(async () => {
		const currentHumanId = get(page).url.searchParams.get('HumanId');
		const currentTransactionId = get(page).url.searchParams.get('TransactionId');
		HumanId = currentHumanId;
		await loadHumanPageData(HumanId, currentTransactionId);
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}

	
	<div class="section">
		
		
		{#if Human.HumanId || HumanId}
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-2">Human Report</h3>
				</div>
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
				</div>
			</div>
			{#if akaNames.length > 0}
				<div class="ActionBox">
					<div class="title-container">
						<h3 class="title is-4">Human Report</h3>
					</div>
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
				</div>
			{/if}

			{#if combinedTimeline && combinedTimeline.data && combinedTimeline.data.combinedTimeLine && combinedTimeline.data.combinedTimeLine.length > 0}
				<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-4">Combined Timeline ({combinedTimeline.data.combinedTimeLine.length} records)</h3>
				</div>
					<div class="table-wrapper">
						<table class="table is-fullwidth is-striped" on:click={handleCombinedTimelineClick}>
							<thead>
								<tr>
									<th>Date</th>
									<th>Description</th>
									<th>Lat/Lng</th>
								</tr>
							</thead>
							<tbody>
								{#each combinedTimeline.data.combinedTimeLine as event}
									<tr>
										<td>{formatDate(event.DateCirca, event.DateAccuracy)}</td>
										<td class="combined-timeline-description">{@html event.Description}</td>
										<td>
											{#if event.Latitude && event.Longitude}
												{event.Latitude}, {event.Longitude}
											{/if}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			{/if}

			

			{#if voyages.length > 0}
				<div class="ActionBox">
					<div class="title-container">
						<h3 class="title is-4">Voyages ({voyages.length} records)</h3>
					</div>
					<div class="table-wrapper">
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
									<tr on:click={() => window.open(`/Voyage?VoyageId=${voyage.VoyageId}`, '_blank')} style="cursor: pointer;">
										<td>{voyage.VoyageId}</td>
										<td>{voyage.RoleId}</td>
										<td>{voyage.Notes || ''}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			{/if}

			{#if transactions.length > 0}
				<div class="ActionBox">
					<div class="title-container">
						<h3 class="title is-4">Transactions ({transactions.length} records)</h3>
					</div>
					<div class="table-wrapper">
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
									<tr on:click={() => window.open(`/Transaction?TransactionId=${txn.TransactionId}`, '_blank')} style="cursor: pointer;">
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
				</div>
			{/if}


		{:else}
			<div class="notification is-warning">
				No Human ID provided. Please provide a HumanId parameter in the URL.
			</div>
		{/if}
	</div>
{/if}
