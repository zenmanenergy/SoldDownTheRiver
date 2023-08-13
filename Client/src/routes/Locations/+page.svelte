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
	const fullLocation = `${location.City} ${location.State} ${location.Country}`.toLowerCase();
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
		<a href="/AdminMenu">Back to Menu</a>
		<div class="ActionBox">
			<h3 class="title is-2">List of Locations</h3>
			<button on:click={addLocation}>Add Location</button>
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
						<th>City</th>
						<th>State</th>
						<th>Country</th>
						<th>Last Modified</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredLocations as location}
						<tr style="cursor: pointer;" on:click={() => go(location.LocationId)}>
							<td>{location.City}</td>
							<td>{location.State}</td>
							<td>{location.Country}</td>
							<td>{moment.utc(location.LastModified).local().fromNow()}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<button on:click={addLocation}>Add Location</button>
		</div>
	</div>
{/if}
	