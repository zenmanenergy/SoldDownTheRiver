<!-- src/routes/Reports/Voyage/+page.svelte -->
<!-- Read-only Voyage Report View -->

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetVoyage } from '../../Voyage/handleGetVoyage.js';
	import { handleGetShips } from '../../Voyage/handleGetShips.js';
	import { handleGetVoyageHumans } from '../../Voyage/handleGetVoyageHumans.js';
	import { handleGetLocations } from '../../Voyage/handleGetLocations.js';
	import { handleGetLinkReferences } from '../../References/handleGetLinkReferences.js';
	import { Session } from "../../Session.js";
	
	let VoyageId = '';
	let Voyage = {
		VoyageId: "", 
		ShipId: "", 
		StartLocationId: "", 
		EndLocationId: "", 
		StartDate: null, 
		EndDate: null, 
		Notes: ""
	};
	let Ships = [];
	let VoyageHumans = [];
	let Locations = [];
	let voyageReferences = [];
	let isLoading = true;
	let isReferencesLoading = true;

	// Define voyage-specific roles for display
	const voyageRoles = [
		{ id: 'Enslaved', name: 'Enslaved' },
		{ id: 'Captain', name: 'Captain' },
		{ id: 'Owner 1', name: 'Owner 1' },
		{ id: 'Owner 2', name: 'Owner 2' },
		{ id: 'Shipping Agent', name: 'Shipping Agent' },
		{ id: 'Collector Agent', name: 'Collector Agent' }
	];

	// Helper function to format birthdate based on accuracy
	function formatBirthDate(date, accuracy) {
		if (!date) return '';
		const mDate = moment(date);
		switch(accuracy) {
			case 'Y': return mDate.format('YYYY');
			case 'M': return mDate.format('YYYY-MM');
			default: return mDate.format('YYYY-MM-DD');
		}
	}

	async function setVoyage(data) {
		if (data.VoyageId) {
			Voyage.VoyageId = data.VoyageId || "";
			Voyage.ShipId = data.ShipId || "";
			Voyage.StartLocationId = data.StartLocationId || "";
			Voyage.CaptainHumanId = data.CaptainHumanId;
			Voyage.EndLocationId = data.EndLocationId || "";
			if (data.StartDate) {
				Voyage.StartDate = moment.utc(data.StartDate).format("YYYY-MM-DD") || "";
			}
			if (data.EndDate) {
				Voyage.EndDate = moment.utc(data.EndDate).format("YYYY-MM-DD") || "";
			}
			Voyage.Notes = data.Notes || "";
		}
	}

	async function setShips(data) {
		Ships = data;
	}

	async function setVoyageHumans(data) {
		VoyageHumans = data;
	}

	async function setLocations(data) {
		Locations = data;
	}

	async function setVoyageReferences(data) {
		voyageReferences = data;
	}

	function getShipName() {
		if (!Voyage.ShipId) return "Unknown";
		const ship = Ships.find(s => s.ShipId === Voyage.ShipId);
		return ship ? ship.ShipName : "Unknown";
	}

	function getLocationName(locationId) {
		if (!locationId) return "Unknown";
		const location = Locations.find(l => l.LocationId === locationId);
		return location ? location.Address : "Unknown";
	}

	function getHumansByRole(role) {
		return VoyageHumans.filter(h => h.Role === role);
	}

	// Utility function to get a URL parameter by name
	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	onMount(async () => {
		await Session.handleSession();
		VoyageId = getURLVariable('VoyageId') || '';
		
		if (!VoyageId) {
			console.error("No VoyageId provided");
			isLoading = false;
			return;
		}
		
		await Promise.all([
			handleGetVoyage(Session.SessionId, VoyageId, setVoyage),
			handleGetShips(Session.SessionId, setShips),
			handleGetVoyageHumans(Session.SessionId, VoyageId, setVoyageHumans),
			handleGetLocations(Session.SessionId, setLocations)
		]);

		await handleGetLinkReferences(VoyageId, 'voyage', setVoyageReferences);
		isReferencesLoading = false;

		isLoading = false;
	});
</script>

<svelte:head>
	<title>Voyage Report - {getShipName()}</title>
</svelte:head>

{#if isLoading}
<div class="loading-screen">
	<div class="spinner"></div>
</div>
{:else}

<div class="section">
	<div class="ActionBox">
		<div class="title-container">
			<h3 class="title is-2">Voyage Report</h3>
		</div>

		<!-- Voyage Information -->
		<div class="content">
			<div class="columns">
				<div class="column is-half">
					<table class="table is-borderless">
						<tbody>
							<tr>
								<td><strong>Voyage ID:</strong></td>
								<td>{Voyage.VoyageId}</td>
							</tr>
							<tr>
								<td><strong>Ship:</strong></td>
								<td>
									<a href="/Reports/Ship?ShipId={Voyage.ShipId}" target="_blank">
										{getShipName()}
									</a>
								</td>
							</tr>
							<tr>
								<td><strong>Start Location:</strong></td>
								<td>
									<a href="/Reports/Location?LocationId={Voyage.StartLocationId}" target="_blank">
										{getLocationName(Voyage.StartLocationId)}
									</a>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
				<div class="column is-half">
					<table class="table is-borderless">
						<tbody>
							<tr>
								<td><strong>Start Date:</strong></td>
								<td>{Voyage.StartDate ? moment.utc(Voyage.StartDate).format('MMMM D, YYYY') : "N/A"}</td>
							</tr>
							<tr>
								<td><strong>End Date:</strong></td>
								<td>{Voyage.EndDate ? moment.utc(Voyage.EndDate).format('MMMM D, YYYY') : "N/A"}</td>
							</tr>
							<tr>
								<td><strong>End Location:</strong></td>
								<td>
									<a href="/Reports/Location?LocationId={Voyage.EndLocationId}" target="_blank">
										{getLocationName(Voyage.EndLocationId)}
									</a>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			{#if Voyage.Notes}
			<div class="field">
				<label class="label">Notes:</label>
				<div class="content">
					<p>{Voyage.Notes}</p>
				</div>
			</div>
			{/if}
		</div>
	</div>

	<!-- Voyage Participants by Role -->
	{#each voyageRoles as role}
		{@const roleHumans = getHumansByRole(role.id)}
		{#if roleHumans.length > 0}
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-4">{role.name} ({roleHumans.length})</h3>
				</div>
				
				<div class="table-container">
					<table class="table is-striped is-hoverable is-fullwidth">
						<thead>
							<tr>
								<th>First Name</th>
								<th>Last Name</th>
								<th>Birth Date</th>
								<th>Racial Descriptor</th>
								<th>Sex</th>
							</tr>
						</thead>
						<tbody>
							{#each roleHumans as human}
								<tr on:click={() => window.location.href = `/Admin/Reports/Human?HumanId=${human.HumanId}`} style="cursor:pointer;">
									<td>{human.FirstName || ''}</td>
									<td>{human.LastName || ''}</td>
									<td>{human.BirthDate ? formatBirthDate(human.BirthDate, human.BirthDateAccuracy) : ''}</td>
									<td>{human.RacialDescriptor || ''}</td>
									<td>{human.Sex || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/if}
	{/each}

	<!-- All Voyage Participants Summary -->
	{#if VoyageHumans.length > 0}
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-4">All Voyage Participants ({VoyageHumans.length})</h3>
			</div>
			
			<div class="table-container">
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th>First Name</th>
							<th>Last Name</th>
							<th>Role</th>
							<th>Birth Date</th>
							<th>Racial Descriptor</th>
							<th>Sex</th>
						</tr>
					</thead>
					<tbody>
						{#each VoyageHumans as human}
							<tr on:click={() => window.location.href = `/Admin/Reports/Human?HumanId=${human.HumanId}`} style="cursor:pointer;">
								<td>{human.FirstName || ''}</td>
								<td>{human.LastName || ''}</td>
								<td><span class="tag is-info">{human.Role || ''}</span></td>
								<td>{human.BirthDate ? formatBirthDate(human.BirthDate, human.BirthDateAccuracy) : ''}</td>
								<td>{human.RacialDescriptor || ''}</td>
								<td>{human.Sex || ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{:else}
		<div class="ActionBox">
			<div class="content">
				<p>No participants recorded for this voyage.</p>
			</div>
		</div>
	{/if}

	<!-- References Section -->
	{#if VoyageId}
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-4">References ({voyageReferences.length})</h3>
			</div>
			{#if isReferencesLoading}
				<div>Loading references...</div>
			{:else if voyageReferences.length === 0}
				<div class="content">
					<p>No references linked to this voyage.</p>
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
							{#each voyageReferences as reference}
								<tr on:click={() => window.location.href = `/Admin/Reports/Reference?ReferenceId=${reference.ReferenceId}`} style="cursor:pointer;">
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

	<!-- Voyage Summary Statistics -->
	<div class="ActionBox">
		<div class="title-container">
			<h3 class="title is-4">Voyage Statistics</h3>
		</div>
		
		<div class="columns">
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-danger">{getHumansByRole('Enslaved').length}</p>
					<p class="subtitle">Enslaved People</p>
				</div>
			</div>
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-info">{getHumansByRole('Captain').length}</p>
					<p class="subtitle">Captain(s)</p>
				</div>
			</div>
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-warning">{getHumansByRole('Owner 1').length + getHumansByRole('Owner 2').length}</p>
					<p class="subtitle">Owner(s)</p>
				</div>
			</div>
			<div class="column">
				<div class="box has-text-centered">
					<p class="title is-1 has-text-success">{getHumansByRole('Shipping Agent').length + getHumansByRole('Collector Agent').length}</p>
					<p class="subtitle">Agent(s)</p>
				</div>
			</div>
		</div>

		{#if Voyage.StartDate && Voyage.EndDate}
			{@const duration = moment(Voyage.EndDate).diff(moment(Voyage.StartDate), 'days')}
			<div class="notification is-info">
				<strong>Voyage Duration:</strong> {duration} days
				({moment(Voyage.StartDate).format('MMMM D, YYYY')} to {moment(Voyage.EndDate).format('MMMM D, YYYY')})
			</div>
		{/if}
	</div>
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

	.notification.is-info {
		margin-top: 1rem;
		text-align: center;
	}

	a {
		color: #3273dc;
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}
</style>
