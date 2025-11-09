<style>
	@import '/static/FormPages.css';

	.field.is-grouped {
		display: flex;
		align-items: flex-end;
		gap: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.field.is-grouped .control.is-expanded {
		flex: 1;
	}

	.field.is-grouped .control {
		margin-bottom: 0;
	}

	.field.is-grouped .input,
	.field.is-grouped .select select {
		height: 2.5rem;
		box-sizing: border-box;
	}

	.field.is-grouped .select {
		height: 2.5rem;
	}
</style>
<script>
import moment from 'moment';
import { onMount } from 'svelte';
import {handleGetLocations} from './handleGetLocations.js';
	import {Session} from "../../Session.js";

let Locations = [];
let filteredLocations = [];
let isLoading = true;
let searchQuery = '';
let filterOption = 'all';

let sortColumn = 'City';
let sortAscending = true;

async function setLocations(data) {
	Locations=data
	
}
onMount(async () => {
		await Session.handleSession();
	await Promise.all([
		await handleGetLocations(Session.SessionId,setLocations)
		
	]);
	isLoading = false;
});
$: filteredLocations = Locations.filter(location => {
	// Filter by approval status
	if (filterOption === 'unapproved' && location.isApproved !== 0) {
		return false;
	}
	
	// Build the City/County string as before.
	const cityCounty = location.City && location.County 
		? `${location.City} ${location.County}` 
		: location.City || location.County || '';
	// Create a single searchable string including Name, Latitude and Longitude.
	const searchableText = [
		location.LocationId || '',
		location.Name || '',
		cityCounty,
		location.State || '',
		location.Country || '',
		location.Latitude != null ? location.Latitude.toString() : '',
		location.Longitude != null ? location.Longitude.toString() : ''
	].join(' ').toLowerCase();
	return searchableText.includes(searchQuery.toLowerCase());
});

$: filteredLocations = [...filteredLocations].sort((a, b) => {
	let valueA = a[sortColumn] ?? '';
	let valueB = b[sortColumn] ?? '';

	// Convert to lowercase for case-insensitive sorting
	if (typeof valueA === 'string') valueA = valueA.toLowerCase();
	if (typeof valueB === 'string') valueB = valueB.toLowerCase();

	if (valueA < valueB) return sortAscending ? -1 : 1;
	if (valueA > valueB) return sortAscending ? 1 : -1;
	return 0;
});

function toggleSort(column) {
	if (sortColumn === column) {
		sortAscending = !sortAscending;
	} else {
		sortColumn = column;
		sortAscending = true;
	}
}

function addLocation() {
	window.location.href = '/Admin/Location?LocationId=';
}
function go(LocationId) {
	window.location.href = `/Admin/Location?LocationId=`+LocationId;
}
</script>
	
{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-2">List of Locations</h3>
				<button class="button is-primary" on:click={addLocation}>Add Location</button>
			</div>
			<form>
				<div class="field is-grouped">
					<div class="control is-expanded">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by city, state, or country" />
					</div>
					<div class="control">
						<div class="select">
							<select bind:value={filterOption}>
								<option value="all">Show all</option>
								<option value="unapproved">Unapproved</option>
							</select>
						</div>
					</div>
				</div>
			</form>
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('Address')}>Address</th>
							<th on:click={() => toggleSort('City')}>City/County</th>
							<th on:click={() => toggleSort('State')}>State</th>
							<th on:click={() => toggleSort('Country')}>Country</th>
						</tr>
					</thead>
					<tbody>
						{#each filteredLocations as location}
							<tr on:click={(event) => {
								if (event.ctrlKey || event.metaKey) {
									console.log("click1")
									window.open(`/Admin/Location?LocationId=${encodeURIComponent(location.LocationId)}`, '_blank');
								} else {
									console.log("click2", "/Admin/Location?LocationId=${location.LocationId}")
									window.location.href = `/Admin/Location?LocationId=${encodeURIComponent(location.LocationId)}`;
								}
							}}>
								<td>{location.Address || ''}</td>
								<td>
									{location.City ? `${location.City}${location.County ? `/${location.County}` : ''}` : (location.County || '')}
								</td>
								<td>{location.State || ''}</td>
								<td>{location.Country || ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			
		</div>
	</div>
{/if}
