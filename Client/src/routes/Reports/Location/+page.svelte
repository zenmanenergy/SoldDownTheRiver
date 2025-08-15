<!-- src/routes/Reports/Location/+page.svelte -->
<svelte:head>
	<!-- Leaflet CSS -->
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
		integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
		crossorigin=""/>
	<!-- Leaflet JavaScript -->
	<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
		integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
		crossorigin=""></script>
</svelte:head>

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
	
	.location-info {
		background-color: #f8f9fa;
		padding: 1.5rem;
		border-radius: 8px;
		margin-bottom: 2rem;
	}
	
	.location-container {
		display: flex;
		gap: 2rem;
		margin-bottom: 2rem;
	}
	
	.location-details {
		flex: 1;
		min-width: 0;
	}
	
	.map-container {
		width: 500px;
		height: 400px;
		border-radius: 8px;
		overflow: hidden;
		border: 1px solid #dbdbdb;
		background-color: #f5f5f5;
		position: relative;
	}
	
	.leaflet-map {
		width: 100%;
		height: 100%;
		border-radius: 8px;
	}
	
	.map-fallback {
		text-align: center;
		color: #666;
		padding: 2rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
	}
	
	@media (max-width: 768px) {
		.location-container {
			flex-direction: column;
		}
		
		.map-container {
			width: 100%;
		}
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
	}
	
	.pagination-controls {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		margin-top: 1rem;
	}
	
	.pagination-controls button {
		padding: 0.5rem 1rem;
		border: 1px solid #dbdbdb;
		background: white;
		cursor: pointer;
		border-radius: 4px;
	}
	
	.pagination-controls button:hover:not(:disabled) {
		background-color: #f5f5f5;
	}
	
	.pagination-controls button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
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
</style>

<script>
	import moment from 'moment';
	import { onMount } from "svelte";
	import { handleGetLocation } from "./handleGetLocation.js";
	import { handleGetLocationTimelines } from "./handleGetLocationTimelines.js";
	import { handleGetTransactionsByLocationId } from "./handleGetTransactionsByLocationId.js";
	import { handleGetVoyagesByLocationId } from "./handleGetVoyagesByLocationId.js";

	let LocationId = "";
	let isLoading = true;
	let timelines = [];
	let transactions = [];
	let voyages = [];
	let mapDiv;
	let leafletMap;
	let marker;
	let Session={};
	Session.SessionId="";

	let Location = {
		LocationId: "",
		Name: "",
		Address: "",
		City: "",
		County: "",
		State: "",
		Country: "",
		Latitude: "",
		Longitude: "",
		LastModified: ""
	};

	async function setLocation(data) {
		Location.LocationId = data.LocationId || "";
		Location.Name = data.Name || "";
		Location.Address = data.Address || "";
		Location.City = data.City || "";
		Location.County = data.County || "";
		Location.State = data.State || "";
		Location.Country = data.Country || "";
		Location.Latitude = data.Latitude || "";
		Location.Longitude = data.Longitude || "";
		Location.LastModified = data.LastModified || "";
		
		// Initialize map after location data is loaded
		if (Location.Latitude && Location.Longitude && mapDiv && window.L) {
			initializeMap();
		}
	}

	function initializeMap() {
		if (leafletMap) {
			leafletMap.remove(); // Clean up existing map
		}

		const lat = parseFloat(Location.Latitude);
		const lng = parseFloat(Location.Longitude);

		// Create map
		leafletMap = L.map(mapDiv).setView([lat, lng], 12);

		// Define base layers
		const modernMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '© OpenStreetMap contributors'
		});

		// Historical map layers that actually work without CORS issues
		// OpenTopoMap - Good for historical context (CORS-friendly)
		const openTopo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
			subdomains: 'abc',
			maxZoom: 17,
			attribution: '© OpenTopoMap contributors'
		});

		// CartoDB Positron (clean, minimal) - CORS-friendly
		const cartoPositron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
			subdomains: 'abcd',
			maxZoom: 19,
			attribution: '© CartoDB, © OpenStreetMap contributors'
		});

		// CartoDB Dark Matter - CORS-friendly
		const cartoDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
			subdomains: 'abcd',
			maxZoom: 19,
			attribution: '© CartoDB, © OpenStreetMap contributors'
		});

		// Watercolor style map - CORS-friendly
		const stamenWatercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg', {
			subdomains: 'abcd',
			maxZoom: 16,
			attribution: '© Stamen Design, © OpenStreetMap contributors'
		});

		// Add default layer
		modernMap.addTo(leafletMap);

		// Create layer control
		const baseLayers = {
			"Modern Map": modernMap,
			"Topographic": openTopo,
			"Clean Light": cartoPositron,
			"Dark Theme": cartoDark,
			"Watercolor": stamenWatercolor
		};

		// Add layer switcher control
		L.control.layers(baseLayers).addTo(leafletMap);

		// Add marker at location
		marker = L.marker([lat, lng]).addTo(leafletMap);
		
		// Add popup with location info
		let popupContent = `<strong>${Location.Name || 'Location'}</strong><br>`;
		if (Location.Address) popupContent += `${Location.Address}<br>`;
		if (Location.City) popupContent += `${Location.City}<br>`;
		popupContent += `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
		
		marker.bindPopup(popupContent);
	}

	async function setTimelines(_timelines) {
		console.log("data", _timelines?.data);
		timelines = (_timelines && _timelines.data) || [];
	}

	async function setTransactions(_transactions) {
		console.log("transactions data", _transactions);
		transactions = _transactions || [];
	}

	async function setVoyages(_voyages) {
		console.log("voyages data", _voyages);
		voyages = _voyages || [];
	}

	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		LocationId = urlParams.get("LocationId") || "";

		if (LocationId) {
			await Promise.all([
				await handleGetLocation(Session.SessionId, LocationId, setLocation)
			]);
			await handleGetLocationTimelines(Session.SessionId, LocationId, setTimelines);
			await handleGetTransactionsByLocationId(Session.SessionId, LocationId, setTransactions);
			await handleGetVoyagesByLocationId(Session.SessionId, LocationId, setVoyages);
		}

		console.log("LocationId", LocationId);
		isLoading = false;
		
		// Initialize map after everything is loaded and Leaflet is available
		setTimeout(() => {
			if (Location.Latitude && Location.Longitude && mapDiv && window.L) {
				initializeMap();
			}
		}, 100);
	});

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

	let currentPage = 1;
	let itemsPerPage = 50;
	let sortKey = '';
	let sortDirection = 'asc';

	// Transaction pagination variables
	let currentTransactionPage = 1;
	let transactionItemsPerPage = 50;
	let transactionSortKey = '';
	let transactionSortDirection = 'asc';

	// Voyage pagination variables
	let currentVoyagePage = 1;
	let voyageItemsPerPage = 50;
	let voyageSortKey = '';
	let voyageSortDirection = 'asc';

	function sortTable(key) {
		if (sortKey === key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDirection = 'asc';
		}
		currentPage = 1;
	}

	function sortTransactionTable(key) {
		if (transactionSortKey === key) {
			transactionSortDirection = transactionSortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			transactionSortKey = key;
			transactionSortDirection = 'asc';
		}
		currentTransactionPage = 1;
	}

	function sortVoyageTable(key) {
		if (voyageSortKey === key) {
			voyageSortDirection = voyageSortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			voyageSortKey = key;
			voyageSortDirection = 'asc';
		}
		currentVoyagePage = 1;
	}

	$: sortedTimelines = [...timelines].sort((a, b) => {
		if (!sortKey) return 0;
		let aValue, bValue;
		if (sortKey === 'Name') {
			aValue = (a.FirstName || '') + ' ' + (a.LastName || '');
			bValue = (b.FirstName || '') + ' ' + (b.LastName || '');
		} else {
			aValue = a[sortKey] || '';
			bValue = b[sortKey] || '';
		}
		if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
		if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
		return 0;
	});

	$: totalPages = Math.ceil(sortedTimelines.length / itemsPerPage);
	$: paginatedTimelines = sortedTimelines.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

	$: sortedTransactions = [...transactions].sort((a, b) => {
		if (!transactionSortKey) return 0;
		let aValue, bValue;
		if (transactionSortKey === 'Date') {
			aValue = a.date_circa || '';
			bValue = b.date_circa || '';
		} else if (transactionSortKey === 'Sellers') {
			aValue = a.Sellers || '';
			bValue = b.Sellers || '';
		} else if (transactionSortKey === 'Buyers') {
			aValue = a.Buyers || '';
			bValue = b.Buyers || '';
		} else {
			aValue = a[transactionSortKey] || '';
			bValue = b[transactionSortKey] || '';
		}
		if (aValue < bValue) return transactionSortDirection === 'asc' ? -1 : 1;
		if (aValue > bValue) return transactionSortDirection === 'asc' ? 1 : -1;
		return 0;
	});

	$: totalTransactionPages = Math.ceil(sortedTransactions.length / transactionItemsPerPage);
	$: paginatedTransactions = sortedTransactions.slice((currentTransactionPage - 1) * transactionItemsPerPage, currentTransactionPage * transactionItemsPerPage);

	$: sortedVoyages = [...voyages].sort((a, b) => {
		if (!voyageSortKey) return 0;
		let aValue, bValue;
		if (voyageSortKey === 'StartDate') {
			aValue = a.StartDate || '';
			bValue = b.StartDate || '';
		} else if (voyageSortKey === 'EndDate') {
			aValue = a.EndDate || '';
			bValue = b.EndDate || '';
		} else if (voyageSortKey === 'ShipName') {
			aValue = a.ShipName || '';
			bValue = b.ShipName || '';
		} else if (voyageSortKey === 'Route') {
			aValue = `${a.StartCity || ''} to ${a.EndCity || ''}`;
			bValue = `${b.StartCity || ''} to ${b.EndCity || ''}`;
		} else if (voyageSortKey === 'Captains') {
			aValue = a.Captains || '';
			bValue = b.Captains || '';
		} else {
			aValue = a[voyageSortKey] || '';
			bValue = b[voyageSortKey] || '';
		}
		if (aValue < bValue) return voyageSortDirection === 'asc' ? -1 : 1;
		if (aValue > bValue) return voyageSortDirection === 'asc' ? 1 : -1;
		return 0;
	});

	$: totalVoyagePages = Math.ceil(sortedVoyages.length / voyageItemsPerPage);
	$: paginatedVoyages = sortedVoyages.slice((currentVoyagePage - 1) * voyageItemsPerPage, currentVoyagePage * voyageItemsPerPage);
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}
	<div class="section">
		<h2 class="report-title">Location Report</h2>
		
		{#if Location.LocationId}
			<div class="location-container">
				<div class="location-details">
					<div class="location-info">
						<h3 class="section-title">Location Information</h3>
						
						{#if Location.Name}
							<div class="info-field">
								<div class="info-label">Name:</div>
								<div class="info-value">{Location.Name}</div>
							</div>
						{/if}
						
						{#if Location.Address}
							<div class="info-field">
								<div class="info-label">Address:</div>
								<div class="info-value">{Location.Address}</div>
							</div>
						{/if}
						
						{#if Location.City}
							<div class="info-field">
								<div class="info-label">City:</div>
								<div class="info-value">{Location.City}</div>
							</div>
						{/if}
						
						{#if Location.County}
							<div class="info-field">
								<div class="info-label">County:</div>
								<div class="info-value">{Location.County}</div>
							</div>
						{/if}
						
						{#if Location.State}
							<div class="info-field">
								<div class="info-label">State:</div>
								<div class="info-value">{Location.State}</div>
							</div>
						{/if}
						
						{#if Location.Country}
							<div class="info-field">
								<div class="info-label">Country:</div>
								<div class="info-value">{Location.Country}</div>
							</div>
						{/if}
						
						{#if Location.Latitude}
							<div class="info-field">
								<div class="info-label">Latitude:</div>
								<div class="info-value">{Location.Latitude}</div>
							</div>
						{/if}
						
						{#if Location.Longitude}
							<div class="info-field">
								<div class="info-label">Longitude:</div>
								<div class="info-value">{Location.Longitude}</div>
							</div>
						{/if}
						
						{#if Location.LastModified}
							<div class="info-field">
								<div class="info-label">Last Modified:</div>
								<div class="info-value">{moment.utc(Location.LastModified).local().format('MMMM Do YYYY, h:mm a')}</div>
							</div>
						{/if}
					</div>
				</div>
				
				{#if Location.Latitude && Location.Longitude}
					<div class="map-container">
						<div bind:this={mapDiv} class="leaflet-map"></div>
					</div>
				{:else}
					<div class="map-container">
						<div class="map-fallback">
							<p>📍</p>
							<p>No coordinates available for this location</p>
						</div>
					</div>
				{/if}
			</div>
		{:else}
			<div class="notification is-warning">
				No location ID provided. Please provide a LocationId parameter in the URL.
			</div>
		{/if}
		
		{#if LocationId && timelines.length}
			<div class="table-wrapper">
				<h3 class="section-title">People Associated with This Location ({timelines.length} records)</h3>
				
				<table class="table is-fullwidth is-striped">
					<thead>
						<tr>
							<th on:click={() => sortTable('Name')} style="cursor:pointer;">
								Name
								{#if sortKey === 'Name'}
									{sortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTable('RoleId')} style="cursor:pointer;">
								Role
								{#if sortKey === 'RoleId'}
									{sortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTable('LocationType')} style="cursor:pointer;">
								Location Type
								{#if sortKey === 'LocationType'}
									{sortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTable('Date_Circa')} style="cursor:pointer;">
								Date Circa
								{#if sortKey === 'Date_Circa'}
									{sortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
						</tr>
					</thead>
					<tbody>
						{#each paginatedTimelines as timeline}
							<tr on:click={() => window.open(`/Human?HumanId=${timeline.HumanId}`, '_blank')} style="cursor: pointer;">
								<td>{timeline.FirstName || ''} {timeline.LastName || ''}</td>
								<td>{timeline.RoleId || ''}</td>
								<td>{timeline.LocationType || ''}</td>
								<td>{formatDate(timeline.Date_Circa, timeline.Date_Accuracy)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
				
				{#if totalPages > 1}
					<div class="pagination-controls">
						<button on:click={() => currentPage = Math.max(1, currentPage - 1)} disabled={currentPage === 1}>
							Previous
						</button>
						<span>Page {currentPage} of {totalPages}</span>
						<button on:click={() => currentPage = Math.min(totalPages, currentPage + 1)} disabled={currentPage === totalPages}>
							Next
						</button>
					</div>
				{/if}
			</div>
		{:else if LocationId && !timelines.length}
			<div class="notification is-info">
				No people records found for this location.
			</div>
		{/if}

		{#if LocationId && transactions.length}
			<div class="table-wrapper">
				<h3 class="section-title">Transactions Associated with This Location ({transactions.length} records)</h3>
				
				<table class="table is-fullwidth is-striped">
					<thead>
						<tr>
							<th on:click={() => sortTransactionTable('Date')} style="cursor:pointer;">
								Date
								{#if transactionSortKey === 'Date'}
									{transactionSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTransactionTable('TransactionType')} style="cursor:pointer;">
								Type
								{#if transactionSortKey === 'TransactionType'}
									{transactionSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTransactionTable('Sellers')} style="cursor:pointer;">
								Sellers
								{#if transactionSortKey === 'Sellers'}
									{transactionSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTransactionTable('Buyers')} style="cursor:pointer;">
								Buyers
								{#if transactionSortKey === 'Buyers'}
									{transactionSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTransactionTable('TotalPrice')} style="cursor:pointer;">
								Price
								{#if transactionSortKey === 'TotalPrice'}
									{transactionSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortTransactionTable('Act')} style="cursor:pointer;">
								Act
								{#if transactionSortKey === 'Act'}
									{transactionSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
						</tr>
					</thead>
					<tbody>
						{#each paginatedTransactions as transaction}
							<tr on:click={() => window.open(`/Admin/Transaction?TransactionId=${transaction.TransactionId}`, '_blank')} style="cursor: pointer;">
								<td>{formatDate(transaction.date_circa, transaction.date_accuracy)}</td>
								<td>{transaction.TransactionType || ''}</td>
								<td>{transaction.Sellers || ''}</td>
								<td>{transaction.Buyers || ''}</td>
								<td>{transaction.TotalPrice ? '$' + transaction.TotalPrice.toLocaleString() : ''}</td>
								<td>{transaction.Act || ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
				
				{#if totalTransactionPages > 1}
					<div class="pagination-controls">
						<button on:click={() => currentTransactionPage = Math.max(1, currentTransactionPage - 1)} disabled={currentTransactionPage === 1}>
							Previous
						</button>
						<span>Page {currentTransactionPage} of {totalTransactionPages}</span>
						<button on:click={() => currentTransactionPage = Math.min(totalTransactionPages, currentTransactionPage + 1)} disabled={currentTransactionPage === totalTransactionPages}>
							Next
						</button>
					</div>
				{/if}
			</div>
		{:else if LocationId && !transactions.length}
			<div class="notification is-info">
				No transaction records found for this location.
			</div>
		{/if}

		{#if LocationId && voyages.length}
			<div class="table-wrapper">
				<h3 class="section-title">Voyages Associated with This Location ({voyages.length} records)</h3>
				
				<table class="table is-fullwidth is-striped">
					<thead>
						<tr>
							<th on:click={() => sortVoyageTable('StartDate')} style="cursor:pointer;">
								Start Date
								{#if voyageSortKey === 'StartDate'}
									{voyageSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortVoyageTable('EndDate')} style="cursor:pointer;">
								End Date
								{#if voyageSortKey === 'EndDate'}
									{voyageSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortVoyageTable('ShipName')} style="cursor:pointer;">
								Ship
								{#if voyageSortKey === 'ShipName'}
									{voyageSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortVoyageTable('Route')} style="cursor:pointer;">
								Route
								{#if voyageSortKey === 'Route'}
									{voyageSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortVoyageTable('Captains')} style="cursor:pointer;">
								Captains
								{#if voyageSortKey === 'Captains'}
									{voyageSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
							<th on:click={() => sortVoyageTable('Agents')} style="cursor:pointer;">
								Agents/Traders
								{#if voyageSortKey === 'Agents'}
									{voyageSortDirection === 'asc' ? '↑' : '↓'}
								{/if}
							</th>
						</tr>
					</thead>
					<tbody>
						{#each paginatedVoyages as voyage}
							<tr on:click={() => window.open(`/Admin/Voyage?VoyageId=${voyage.VoyageId}`, '_blank')} style="cursor: pointer;">
								<td>{formatDate(voyage.StartDate, 'D')}</td>
								<td>{formatDate(voyage.EndDate, 'D')}</td>
								<td>{voyage.ShipName || ''}</td>
								<td>{voyage.StartCity || ''}{voyage.StartState ? ', ' + voyage.StartState : ''} → {voyage.EndCity || ''}{voyage.EndState ? ', ' + voyage.EndState : ''}</td>
								<td>{voyage.Captains || ''}</td>
								<td>{[voyage.Agents, voyage.Traders].filter(Boolean).join(', ')}</td>
							</tr>
						{/each}
					</tbody>
				</table>
				
				{#if totalVoyagePages > 1}
					<div class="pagination-controls">
						<button on:click={() => currentVoyagePage = Math.max(1, currentVoyagePage - 1)} disabled={currentVoyagePage === 1}>
							Previous
						</button>
						<span>Page {currentVoyagePage} of {totalVoyagePages}</span>
						<button on:click={() => currentVoyagePage = Math.min(totalVoyagePages, currentVoyagePage + 1)} disabled={currentVoyagePage === totalVoyagePages}>
							Next
						</button>
					</div>
				{/if}
			</div>
		{:else if LocationId && !voyages.length}
			<div class="notification is-info">
				No voyage records found for this location.
			</div>
		{/if}
	</div>
{/if}
