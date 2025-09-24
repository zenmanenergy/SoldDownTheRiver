<!-- src/routes/Reports/Human/+page.svelte -->


<style>
	@import "/static/FormPages.css";
	
</style>

<script>
// Compute timelineLocations for TimelineMap
$: timelineLocations = (combinedTimeline && combinedTimeline.data && combinedTimeline.data.combinedTimeLine)
	? combinedTimeline.data.combinedTimeLine
		.filter(e => e.Latitude && e.Longitude)
		.map((e, i) => ({
			...e,
			LocationId: e.LocationId || `timeline-${i}`,
			Latitude: parseFloat(e.Latitude),
			Longitude: parseFloat(e.Longitude)
		}))
	: [];
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
	import FamilyTreeCanvas from '../../../components/FamilyTreeCanvas.svelte';
	import { handleGetFamilies } from './handleGetFamilies.js';
	import TimelineMap from '../../../components/TimelineMap.svelte';

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
	let families = [];

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
			case 'd': return 'Day';
			case 'm': return 'Month';
			case 'y': return 'Year';
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
			console.log("combinedTimelinecombinedTimeline",combinedTimeline)
			const humanTransactions = await handleGetHumanTransactions(HumanId);
			if (humanTransactions) {
				transactions = humanTransactions;
			}

			await handleGetAKA(HumanId, (data) => {
				akaNames = data || [];
			});

			await handleGetFamilies(null, HumanId, (data) => {
				families = data || [];
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

	// Add keyboard event handlers for accessibility
	function handleKeyDown(event) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleClick(event);
		}
	}
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
					<h3 class="title is-2">{Human.isCompany ? 'Company' : 'Human'} Report</h3>
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
					
					
					{#if Human.isCompany}
						<div class="info-field">
							<div class="info-label">Company Name:</div>
							<div class="info-value">{Human.FirstName}</div>
						</div>
					{:else}
						{#if Human.FirstName || Human.MiddleName || Human.LastName}
							<div class="info-field">
								<div class="info-label">Name:</div>
								<div class="info-value">{Human.FirstName} {Human.MiddleName} {Human.LastName}

									{#if akaNames.length > 0}
										<div class="aka-item">
											Also known as:
											{#each akaNames as aka, index}
												{#if Human.isCompany}
													{aka.AKAFirstName}{index < akaNames.length - 1 ? ', ' : ''}
												{:else}
													{aka.AKAFirstName} {aka.AKAMiddleName || ''} {aka.AKALastName}{index < akaNames.length - 1 ? ', ' : ''}
												{/if}
											{/each}
										</div>
									{/if}
								</div> 
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
								</div>b
							</div>
						{/if}
					{/if}
				</div>
			</div>
			

			{#if combinedTimeline && combinedTimeline.data && combinedTimeline.data.combinedTimeLine && combinedTimeline.data.combinedTimeLine.length > 0}
				<div class="ActionBox">
					<div class="title-container">
						<h3 class="title is-4">Combined Timeline ({combinedTimeline.data.combinedTimeLine.length} records)</h3>
					</div>
					<div class="columns">
						<div class="column is-half">
							<div class="table-container">
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
						<div class="column is-half">
							<TimelineMap Voyage={{}} Locations={timelineLocations} />
						</div>
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
									<tr 
										on:click={() => window.open(`/Voyage?VoyageId=${voyage.VoyageId}`, '_blank')} 
										on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') window.open(`/Voyage?VoyageId=${voyage.VoyageId}`, '_blank'); }}
										tabindex="0"
										style="cursor: pointer;"
									>
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

			{#if families.length > 0}
				<h3 class="title is-3">Family Tree</h3>
				<FamilyTreeCanvas {families} BaseHref="/Reports/Human" />
			{:else}
				<div class="notification is-warning">
					No family relationships defined.
				</div>
			{/if}

		{:else}
			<div class="notification is-warning">
				No Human ID provided. Please provide a HumanId parameter in the URL.
			</div>
		{/if}
	</div>
{/if}
