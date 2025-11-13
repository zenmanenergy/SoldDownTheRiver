<!-- src/routes/Reports/Ship/+page.svelte -->
<!-- Read-only Ship Report View -->

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetShip } from './handleGetShip.js';
	import { handleGetShipVoyages } from './handleGetShipVoyages.js';
	import { handleGetLocations } from './handleGetLocations.js';
	import { handleGetLinkReferences } from '../References/handleGetLinkReferences.js';
	
	let ShipId = "";
	let Ship = {
		ShipId: "", 
		ShipName: "", 
		BuildDate: null, 
		Notes: "", 
		ShipType: "", 
		Size: "", 
		HomePortLocationId: "",
		AgentHumanId: ""
	};
	let Voyages = [];
	let Locations = [];
	let shipReferences = [];
	let isReferencesLoading = true;
	let isLoading = true;

	// Pagination and sorting for Voyages
	let voyagesCurrentPage = 1;
	let voyagesItemsPerPage = 10;
	let voyagesSortField = 'StartDate';
	let voyagesSortDirection = 'desc';

	$: voyagesTotalPages = Math.ceil(Voyages.length / voyagesItemsPerPage);

	$: paginatedVoyages = Voyages
		.sort((a, b) => {
			let aVal = a[voyagesSortField] || '';
			let bVal = b[voyagesSortField] || '';
			
			if (voyagesSortField.includes('Date')) {
				aVal = new Date(aVal || 0);
				bVal = new Date(bVal || 0);
			}
			
			if (voyagesSortDirection === 'asc') {
				return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
			} else {
				return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
			}
		})
		.slice((voyagesCurrentPage - 1) * voyagesItemsPerPage, voyagesCurrentPage * voyagesItemsPerPage);

	async function setShip(data) {
		Ship.ShipId = data.ShipId || "";
		Ship.ShipName = data.ShipName || "";
		if (data.BuildDate) {
			Ship.BuildDate = moment.utc(data.BuildDate).format("YYYY-MM-DD") || "";
		}
		Ship.Notes = data.Notes || "";
		Ship.ShipType = data.ShipType || "";
		Ship.Size = data.Size || "";
		Ship.HomePortLocationId = data.HomePortLocationId || "";
		Ship.AgentHumanId = data.AgentHumanId || "";
		console.log("Ship", Ship);
	}

	async function setLocations(data) {
		Locations = data;
	}

	async function setVoyages(data) {
		Voyages = data;
	}

	async function setShipReferences(data) {
		shipReferences = data;
	}

	function sortVoyages(field) {
		if (voyagesSortField === field) {
			voyagesSortDirection = voyagesSortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			voyagesSortField = field;
			voyagesSortDirection = 'asc';
		}
		voyagesCurrentPage = 1;
	}

	function getHomePortDisplay() {
		if (!Ship.HomePortLocationId) return "Unknown";
		const location = Locations.find(loc => loc.LocationId === Ship.HomePortLocationId);
		return location ? location.Address : "Unknown";
	}
	
	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		ShipId = urlParams.get("ShipId") || "";
		
		if (!ShipId) {
			console.error("No ShipId provided");
			isLoading = false;
			return;
		}

		await Promise.all([
			handleGetShip( ShipId, setShip),
			handleGetShipVoyages( ShipId, setVoyages),
			handleGetLocations( setLocations)
		]);

		// Fetch references linked to this ship
		await handleGetLinkReferences(ShipId, 'ship', setShipReferences);
		isReferencesLoading = false;
		
		isLoading = false;
	});
</script>

<svelte:head>
	<title>Ship Report - {Ship.ShipName}</title>
</svelte:head>

{#if isLoading}
<div class="loading-screen">
	<div class="spinner"></div>
</div>
{:else}

<div class="section">
	<div class="ActionBox">
		<div class="title-container">
			<h3 class="title is-2">Ship Report: {Ship.ShipName}</h3>
		</div>

		<!-- Ship Information -->
		<div class="content">
			<div class="columns">
			   <div class="column is-half">
				   <table class="table is-borderless">
					   <tbody>
						   {#if Ship.ShipName}
						   <tr>
							   <td><strong>Ship Name:</strong></td>
							   <td>{Ship.ShipName}</td>
						   </tr>
						   {/if}
						   {#if Ship.ShipType}
						   <tr>
							   <td><strong>Ship Type:</strong></td>
							   <td>{Ship.ShipType}</td>
						   </tr>
						   {/if}
						   {#if Ship.Size}
						   <tr>
							   <td><strong>Size:</strong></td>
							   <td>{Ship.Size}</td>
						   </tr>
						   {/if}
					   </tbody>
				   </table>
			   </div>
			   <div class="column is-half">
				   <table class="table is-borderless">
					   <tbody>
						   {#if Ship.BuildDate}
						   <tr>
							   <td><strong>Build Date:</strong></td>
							   <td>{moment.utc(Ship.BuildDate).format('MMMM D, YYYY')}</td>
						   </tr>
						   {/if}
						   {#if getHomePortDisplay() && getHomePortDisplay() !== 'Unknown'}
						   <tr>
							   <td><strong>Home Port:</strong></td>
							   <td>{getHomePortDisplay()}</td>
						   </tr>
						   {/if}
					   </tbody>
				   </table>
			   </div>
			</div>

			{#if Ship.Notes}
			<div class="field">
				<label class="label">Notes:</label>
				<div class="content">
					<p>{Ship.Notes}</p>
				</div>
			</div>
			{/if}
		</div>
	</div>

	<!-- Voyages Section -->
	<div class="ActionBox">
		<div class="title-container">
			<h3 class="title is-4">Voyages ({Voyages.length})</h3>
		</div>
		
		{#if Voyages.length === 0}
			<div class="content">
				<p>No voyages recorded for this ship.</p>
			</div>
		{:else}
			<div class="table-container">
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th>
								<button class="button is-ghost" on:click={() => sortVoyages('StartDate')}>
									Start Date
									{#if voyagesSortField === 'StartDate'}
										<span class="icon is-small">
											<i class="fas fa-chevron-{voyagesSortDirection === 'asc' ? 'up' : 'down'}"></i>
										</span>
									{/if}
								</button>
							</th>
							<th>From</th>
							<th>
								<button class="button is-ghost" on:click={() => sortVoyages('EndDate')}>
									End Date
									{#if voyagesSortField === 'EndDate'}
										<span class="icon is-small">
											<i class="fas fa-chevron-{voyagesSortDirection === 'asc' ? 'up' : 'down'}"></i>
										</span>
									{/if}
								</button>
							</th>
							<th>To</th>
						</tr>
					</thead>
					<tbody>
						{#each paginatedVoyages as voyage}
							<tr on:click={() => window.location.href = `/Reports/Voyage?VoyageId=${voyage.VoyageId}`} style="cursor:pointer;">
								<td>{voyage.StartDate ? moment.utc(voyage.StartDate).format('MMMM D, YYYY') : "N/A"}</td>
								<td>{voyage.StartCity} {voyage.StartState}</td>
								<td>{voyage.EndDate ? moment.utc(voyage.EndDate).format('MMMM D, YYYY') : "N/A"}</td>
								<td>{voyage.EndCity} {voyage.EndState}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Voyages Pagination -->
			{#if voyagesTotalPages > 1}
			<nav class="pagination is-centered" role="navigation">
				<button 
					class="pagination-previous" 
					disabled={voyagesCurrentPage === 1}
					on:click={() => voyagesCurrentPage = Math.max(1, voyagesCurrentPage - 1)}
				>
					Previous
				</button>
				<button 
					class="pagination-next" 
					disabled={voyagesCurrentPage === voyagesTotalPages}
					on:click={() => voyagesCurrentPage = Math.min(voyagesTotalPages, voyagesCurrentPage + 1)}
				>
					Next
				</button>
				<ul class="pagination-list">
					{#each Array(voyagesTotalPages).fill().map((_, i) => i + 1) as page}
						{#if page === voyagesCurrentPage || page === 1 || page === voyagesTotalPages || Math.abs(page - voyagesCurrentPage) <= 1}
							<li>
								<button 
									class="pagination-link {page === voyagesCurrentPage ? 'is-current' : ''}"
									on:click={() => voyagesCurrentPage = page}
								>
									{page}
								</button>
							</li>
						{:else if page === voyagesCurrentPage - 2 || page === voyagesCurrentPage + 2}
							<li><span class="pagination-ellipsis">&hellip;</span></li>
						{/if}
					{/each}
				</ul>
			</nav>
			{/if}
		{/if}
	</div>

	<!-- References Section -->
	{#if ShipId}
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-4">References ({shipReferences.length})</h3>
			</div>
			{#if isReferencesLoading}
				<div>Loading references...</div>
			{:else if shipReferences.length === 0}
				<div class="content">
					<p>No references linked to this ship.</p>
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
							{#each shipReferences as reference}
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

	.button.is-ghost {
		border: none;
		background: none;
		padding: 0;
		font-weight: bold;
		color: #363636;
		text-align: left;
		width: 100%;
		justify-content: flex-start;
	}

	.button.is-ghost:hover {
		background-color: #f5f5f5;
	}

	tr:hover {
		background-color: #f5f5f5;
	}

	.pagination {
		margin-top: 1rem;
	}

	.table.is-borderless td {
		border: none;
		padding: 0.5rem 0.75rem;
	}

	.table.is-borderless tbody tr:last-child td {
		border-bottom: none;
	}
</style>
