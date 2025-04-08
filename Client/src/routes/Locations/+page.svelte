<style>
	@import '/static/FormPages.css';
</style>
<script>
import moment from 'moment';
import { onMount } from 'svelte';
import {handleGetLocations} from './handleGetLocations.js';
	import {Session} from "../Session.js";

let Locations = [];
let filteredLocations = [];
let isLoading = true;
let searchQuery = '';

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
	// Build the City/County string as before.
	const cityCounty = location.City && location.County 
		? `${location.City} ${location.County}` 
		: location.City || location.County || '';
	// Create a single searchable string including Name, Latitude and Longitude.
	const searchableText = [
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
	window.location.href = '/Location?LocationId=';
}
function go(LocationId) {
	window.location.href = `/Location?LocationId=`+LocationId;
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
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by city, state, or country" />
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
									window.open(`/Location?LocationId=${encodeURIComponent(location.LocationId)}`, '_blank');
								} else {
									console.log("click2", "/Location?LocationId=${location.LocationId}")
									window.location.href = `/Location?LocationId=${encodeURIComponent(location.LocationId)}`;
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
