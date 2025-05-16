<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { Session } from "../Session.js";
	import { handleGetReferences } from './handleGetReferences.js';

	let References = [];
	let filteredReferences = [];
	let isLoading = true;
	let searchQuery = '';

	let currentPage = 1;
	let itemsPerPage = 50;
	let totalPages = 1;

	let sortColumn = 'URL';
	let sortAscending = true;

	function getSearchQueryFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("search") || '';
	}

	onMount(async () => {
		searchQuery = getSearchQueryFromURL();
		await Session.handleSession();
		await handleGetReferences(Session.SessionId, setReferences);
		isLoading = false;
	});

	function setReferences(data) {
		References = data;
	}

	function formatDate(date) {
		if (!date) return '';
		return moment.utc(date).format('YYYY-MM-DD HH:mm');
	}

	$: {
		filteredReferences = References.filter(reference => {
			const search = searchQuery.toLowerCase();
			const values = [
				reference.ReferenceId,
				reference.URL,
				reference.Notes,
				formatDate(reference.dateUpdated)
			];
			return values.some(value => value && value.toLowerCase().includes(search));
		});

		filteredReferences.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Handle date sorting
			if (sortColumn === 'dateUpdated') {
				valueA = a.dateUpdated ? new Date(a.dateUpdated) : new Date(0);
				valueB = b.dateUpdated ? new Date(b.dateUpdated) : new Date(0);
			}

			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});

		currentPage = 1;
		totalPages = Math.max(1, Math.ceil(filteredReferences.length / itemsPerPage));
	}

	$: displayedReferences = filteredReferences.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	function addReference() {
		window.location.href = '/Reference?ReferenceId=';
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
				<h3 class="title is-2">List of References</h3>
				<button class="button is-primary" on:click={addReference}>Add Reference</button>
			</div>
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search references" />
					</div>
				</div>
			</form>
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
						<th on:click={() => toggleSort('URL')}>URL</th>
						<th on:click={() => toggleSort('Notes')}>Notes</th>
						<th on:click={() => toggleSort('dateUpdated')}>Date Updated</th>
					</tr>
				</thead>
				<tbody>
					{#each displayedReferences as reference}
						<tr on:click={() => window.location.href = `/Reference?ReferenceId=${reference.ReferenceId}`}>
							<td>{reference.URL || ''}</td>
							<td>{reference.Notes || ''}</td>
							<td>{formatDate(reference.dateUpdated) || ''}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="pagination">
				<button on:click={() => currentPage = Math.max(currentPage - 1, 1)} disabled={currentPage === 1}>
					Previous
				</button>
				<span>{currentPage} / {totalPages}</span>
				<button on:click={() => currentPage = Math.min(currentPage + 1, totalPages)} disabled={currentPage === totalPages}>
					Next
				</button>
			</div>
		</div>
	</div>
{/if}