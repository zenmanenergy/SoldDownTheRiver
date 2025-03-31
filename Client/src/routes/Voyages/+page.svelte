<style>
	@import '/static/FormPages.css';
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import {handleGetVoyages} from './handleGetVoyages.js';
	import { Session } from "../Session.js";

	export let Voyages = [];
	let isLoading = true;
	let sortColumn = 'ShipName';
	let sortAscending = true;

	async function setVoyages(data) {
		Voyages = data;
	} 

	onMount(async () => {
		await Session.handleSession();
		await Promise.all([
			handleGetVoyages(Session.SessionId, setVoyages),

		]);
		isLoading = false;
	});

	function addVoyage() {
		window.location.href = '/Voyage?VoyageId=';
	}

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	$: Voyages = [...Voyages].sort((a, b) => {
		let valueA = a[sortColumn] ?? '';
		let valueB = b[sortColumn] ?? '';

		// Handle date sorting separately
		if (sortColumn === 'StartDate' || sortColumn === 'EndDate') {
			valueA = a[sortColumn] ? new Date(a[sortColumn]) : new Date(0);
			valueB = b[sortColumn] ? new Date(a[sortColumn]) : new Date(0);
		}

		// Convert to lowercase for case-insensitive sorting
		if (typeof valueA === 'string') valueA = valueA.toLowerCase();
		if (typeof valueB === 'string') valueB = valueB.toLowerCase();

		if (valueA < valueB) return sortAscending ? -1 : 1;
		if (valueA > valueB) return sortAscending ? 1 : -1;
		return 0;
	});
</script>

<div class="section">
	{#if isLoading}
		<div class="loading-screen">
			<div class="spinner"></div>
		</div>
	{:else}
		
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-2">List of Voyages</h3>
				<button class="button is-primary"   on:click={addVoyage}>Add Voyage</button>
			</div>
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
							<th on:click={() => toggleSort('ShipName')} style="cursor: pointer;">Ship</th>
							<th on:click={() => toggleSort('StartDate')} style="cursor: pointer;">From</th>
							<th on:click={() => toggleSort('EndDate')} style="cursor: pointer;">To</th>
					</tr>
				</thead>
				<tbody>
					{#each Voyages as Voyage}
						<tr on:click={(event) => {
							if (event.ctrlKey || event.metaKey) {
								window.open(`/Voyage?VoyageId=${encodeURIComponent(Voyage.VoyageId)}`, '_blank');
							} else {
								location.href=`/Voyage?VoyageId=${encodeURIComponent(Voyage.VoyageId)}`;
							}
						}}>
							<td>{Voyage.ShipName}</td>
							<td>{Voyage.StartCity} {Voyage.StartState} {moment(Voyage.StartDate).format('MMMM D, YYYY')}</td>
							<td>{Voyage.EndCity} {Voyage.EndState} {moment(Voyage.EndDate).format('MMMM D, YYYY')}</td>
						</tr>
					{/each}

					
				</tbody>
			</table>
		</div>
	{/if}
</div>
