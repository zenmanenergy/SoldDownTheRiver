<style>
	@import '/static/FormPages.css';
	/* Remove any redundant row styling */
</style>
<script>
	

import moment from 'moment';
import { onMount } from 'svelte';
import {handleGetBusinesses} from './handleGetBusinesses.js';
import {Session} from "../Session.js";


let businesses = [];
let isLoading = true;
let filteredBusinesses = [];
let searchQuery = '';

let sortColumn = 'BusinessName';
let sortAscending = true;

function toggleSort(column) {
	if (sortColumn === column) {
		sortAscending = !sortAscending;
	} else {
		sortColumn = column;
		sortAscending = true;
	}
}

async function setGetBusinesses(data) {
	businesses = data;
}

onMount(async () => {
	await Session.handleSession();
	await Promise.all([
		await handleGetBusinesses(Session.SessionId, setGetBusinesses),
	]);
	isLoading = false;
});

$: filteredBusinesses = businesses.filter(business => business.BusinessName.toLowerCase().includes(searchQuery.toLowerCase()));

$: filteredBusinesses = [...filteredBusinesses].sort((a, b) => {
	let valueA = a[sortColumn] ?? '';
	let valueB = b[sortColumn] ?? '';

	// Handle date sorting separately
	if (sortColumn === 'LastModified') {
		valueA = a.LastModified ? new Date(a.LastModified) : new Date(0);
		valueB = b.LastModified ? new Date(b.LastModified) : new Date(0);
	}

	// Convert to lowercase for case-insensitive sorting
	if (typeof valueA === 'string') valueA = valueA.toLowerCase();
	if (typeof valueB === 'string') valueB = valueB.toLowerCase();

	if (valueA < valueB) return sortAscending ? -1 : 1;
	if (valueA > valueB) return sortAscending ? 1 : -1;
	return 0;
});

function addBusiness() {
	window.location.href = '/Business?BusinessId=';
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
				<h3 class="title is-2">List of Businesses</h3>
				<button class="button is-primary" on:click={addBusiness}>Add Business</button>
			</div>
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by business name" />
					</div>
				</div>
			</form>
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
						<th on:click={() => toggleSort('BusinessName')}>Business Name</th>
						<th on:click={() => toggleSort('LastModified')}>Last Modified</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredBusinesses as business}
						<tr on:click={() => location.href=`/Business?BusinessId=${business.BusinessId}`}>
							<td>{business.BusinessName}</td>
							<td>{moment.utc(business.LastModified).local().fromNow()}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<button class="button is-primary" on:click={addBusiness}>Add Business</button>
		</div>
	</div>
{/if}


