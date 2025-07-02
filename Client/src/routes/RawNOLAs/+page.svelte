<style>
	@import '/static/FormPages.css';

	table {
		width: 100%;
		border-collapse: collapse;
	}

	th, td {
		padding: 8px;
		text-align: left;
		border-bottom: 1px solid #ddd;
	}

	th {
		background-color: #f2f2f2;
		white-space: nowrap;
		cursor: pointer;
	}

	th:hover {
		background-color: #e0e0e0;
	}

	td {
		white-space: nowrap;
	}

</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetRawNolas } from './handleGetRawNolas.js';
	import { Session } from "../Session.js";

	let rawRecords = [];
	let filteredRecords = [];
	let isLoading = true;
	let searchQuery = '';

	// Default sort by DateOfTransaction
	let sortColumn = 'DateOfTransaction';
	let sortAscending = true;

	async function setRecords(data) {
		rawRecords = [...data]; // Ensure reactivity
	}

	onMount(async () => {
		await Session.handleSession();
		if (Session.SessionId) {
			await handleGetRawNolas(Session.SessionId, setRecords);
		}
		isLoading = false;
	});

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	// Format DateOfTransaction to display only the date component
	function formatDateOfTransaction(date) {
		if (!date) return '';
		const parsed = moment.utc(date);
		return parsed.isValid() ? parsed.format('YYYY-MM-DD') : 'Invalid Date';
	}

	// Filter rawRecords using several fields including NOLA_ID (hidden)
	$: filteredRecords = rawRecords
		.filter(record => {
			const fullRecord = `
				${record.FirstParty}
				${record.LocationFirstParty}
				${record.SecondParty}
				${record.LocationSecondParty}
				${record.TypeOfTransaction}
				${record.DateOfTransaction}
				${record.Act}
				${record.Page}
				${record.NotaryPublic}
				${record.Volume}
				${record.NameOfTranscriber}
				${record.Notes}
				${record.Parsed_Notes}
				${record.Error_Notes}
				${record.NOLA_ID}
			`.toLowerCase();
			return fullRecord.includes(searchQuery.toLowerCase());
		})
		.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// For DateOfTransaction, treat values as dates
			if (sortColumn === 'DateOfTransaction') {
				valueA = a.DateOfTransaction ? new Date(a.DateOfTransaction) : new Date(0);
				valueB = b.DateOfTransaction ? new Date(b.DateOfTransaction) : new Date(0);
			}

			// Convert strings to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});
	
	function addRawRecord() {
		// Navigate to a page to add a new raw_nola record.
		window.location.href = '/RawNOLA?NOLA_ID=';
		
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
				<h3 class="title is-2">List of Raw NOLA Records</h3>
				<button class="button is-primary" on:click={addRawRecord}>Add Record</button>
			</div>
			
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search raw records..." />
					</div>
				</div>
			</form>
			
			<table>
				<thead>
					<tr>
						<th on:click={() => toggleSort('FirstParty')}>First Party</th>
						<th on:click={() => toggleSort('LocationFirstParty')}>Location (First Party)</th>
						<th on:click={() => toggleSort('SecondParty')}>Second Party</th>
						<th on:click={() => toggleSort('LocationSecondParty')}>Location (Second Party)</th>
						<th on:click={() => toggleSort('TypeOfTransaction')}>Type</th>
						<th on:click={() => toggleSort('DateOfTransaction')}>Date of Transaction</th>
						<th on:click={() => toggleSort('Act')}>Act</th>
						<th on:click={() => toggleSort('Page')}>Page</th>
						<th on:click={() => toggleSort('NotaryPublic')}>Notary Public</th>
						<th on:click={() => toggleSort('Volume')}>Volume</th>
						<th on:click={() => toggleSort('NameOfTranscriber')}>Transcriber</th>
						<th on:click={() => toggleSort('ReferenceURL')}>Reference URL</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredRecords as record}
						<tr style="cursor: pointer;" on:click={() => location.href=`/RawNOLA?NOLA_ID=${encodeURIComponent(record.NOLA_ID)}`}>
							<td>{record.FirstParty || ''}</td>
							<td>{record.LocationFirstParty || ''}</td>
							<td>{record.SecondParty || ''}</td>
							<td>{record.LocationSecondParty || ''}</td>
							<td>{record.TypeOfTransaction || ''}</td>
							<td>{formatDateOfTransaction(record.DateOfTransaction)}</td>
							<td>{record.Act || ''}</td>
							<td>{record.Page || ''}</td>
							<td>{record.NotaryPublic || ''}</td>
							<td>{record.Volume || ''}</td>
							<td>{record.NameOfTranscriber || ''}</td>
							<td>
								{#if record.ReferenceURL}
									<a href={record.ReferenceURL} target="_blank">View</a>
								{/if}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
{/if}
