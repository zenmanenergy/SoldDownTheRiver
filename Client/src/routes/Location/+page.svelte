<!-- src/routes/Locations/+page.svelte -->
<style>
	@import "/static/FormPages.css";
</style>

<script>
	import moment from 'moment';
	import { onMount } from "svelte";
	import { handleSave } from "./handleSave.js";
	import { handleDelete } from "./handleDelete.js";
	import { handleGetLocation } from "./handleGetLocation.js";
	import { handleGetLocationTimelines } from "./handleGetLocationTimelines.js";
	import {Session} from "../Session.js";

	let LastModified = '';
	let LocationId = "";
	let Address = "";
	let City = "";
	let County = "";
	let State = "";
	let Country = "";
	let Latitude = "";
	let Longitude = "";
	let formValid = false;
	let isLoading = true;
	let timelines=[]

	let Location = {
		LocationId: "",
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
	}

	$: {
		formValid = Location.City; // Adjust if Address or County should be required
	}

	async function setTimelines(_timelines){
		console.log("data", _timelines?.data);
		timelines = (_timelines && _timelines.data) || []; // Ensure timelines is always an array
	}

	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		LocationId = urlParams.get("LocationId") || "";

		if (LocationId) {
			await Promise.all([
				await handleGetLocation(Session.SessionId, LocationId, setLocation)
			]);
			await handleGetLocationTimelines(Session.SessionId, LocationId, setTimelines)
		}

		console.log("LocationId", LocationId);
		isLoading = false;
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

	function sortTable(key) {
		if (sortKey === key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDirection = 'asc';
		}
		currentPage = 1;
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
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}
	<div class="section">
		<div class="ActionBox">
			<form>
				<div class="title-container">
					<h3 class="title is-2">Add/Edit a Location</h3>
					{#if LocationId.length}
						<button class="button is-danger" on:click={() => handleDelete(Session.SessionId, LocationId)}>Delete</button>
					{/if}
				</div>
				
				<input type="hidden" bind:value={Location.LocationId} />

				<div class="field">
					<label class="label" for="Name">Name</label>
					<div class="control">
						<input class="input" type="text" id="Name" placeholder="Enter Name" bind:value={Location.Name}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Address">Address</label>
					<div class="control">
						<input class="input" type="text" id="Address" placeholder="Enter Address" bind:value={Location.Address}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="City">City</label>
					<div class="control">
						<input class="input" type="text" id="City" placeholder="Enter City Name" bind:value={Location.City}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="County">County</label>
					<div class="control">
						<input class="input" type="text" id="County" placeholder="Enter County Name" bind:value={Location.County} />
					</div>
				</div>

				<div class="field">
					<label class="label" for="State">State</label>
					<div class="control">
						<input class="input" type="text" id="State" placeholder="Enter State Name" bind:value={Location.State} />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Country">Country</label>
					<div class="control">
						<input class="input" type="text" id="Country" placeholder="Enter Country Name" bind:value={Location.Country} />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Latitude">Latitude</label>
					<div class="control">
						<input class="input" type="number" id="Latitude" placeholder="Enter Latitude" bind:value={Location.Latitude} step="any" />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Longitude">Longitude</label>
					<div class="control">
						<input class="input" type="number" id="Longitude" placeholder="Enter Longitude" bind:value={Location.Longitude}  step="any" />
					</div>
				</div>

				<div class="field">
					<div class="control">
						<button class="button is-primary" on:click={() => handleSave(Session.SessionId, Location, formValid)}>Save</button>
						
					</div>
				</div>
			</form>

			{#if LastModified}
				<small>Last Modified: {moment.utc(LastModified).local().fromNow()}</small>
			{/if}
		</div>
	</div>
	{#if LocationId && timelines.length}
		<div class="section">
			<table class="table">
				<thead>
					<tr>
							<th on:click={() => sortTable('Name')} style="cursor:pointer;">Name</th>
							<th on:click={() => sortTable('RoleId')} style="cursor:pointer;">Role</th>
							<th on:click={() => sortTable('LocationType')} style="cursor:pointer;">Location Type</th>
							<th on:click={() => sortTable('Date_Circa')} style="cursor:pointer;">Date Circa</th>
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
					<button on:click={() => currentPage = Math.max(1, currentPage - 1)} disabled={currentPage === 1}>Previous</button>
					<span>Page {currentPage} of {totalPages}</span>
					<button on:click={() => currentPage = Math.min(totalPages, currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
				</div>
			{/if}
		</div>
	{/if}
{/if}
