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
	const cityCounty = location.City && location.County 
		? `${location.City} ${location.County}` 
		: location.City || location.County || ''; // Prefer City, fallback to County
	
	const fullLocation = `${cityCounty} ${location.State} ${location.Country}`.toLowerCase();
	return fullLocation.includes(searchQuery.toLowerCase());
});


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
		<a href="/">Back to Menu</a>
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
			<table width=100%>
				<thead>
					<tr>
						<th>Address</th>
						<th>City/County</th> <!-- Updated header -->
						<th>State</th>
						<th>Country</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredLocations as location}
						<tr style="cursor: pointer;" on:click={() => go(location.LocationId)}>
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
	