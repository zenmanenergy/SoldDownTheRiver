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

	.location {
		white-space: normal;
	}

	.pagination {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-top: 1rem;
		gap: 1rem;
	}
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetTransactions } from './handleGetTransactions.js';
	import { Session } from "../../Session.js";

	let Transactions = [];
	let filteredTransactions = [];
	let isLoading = true;
	let searchQuery = '';

	let sortColumn = 'date_circa';
	let sortAscending = true;

	let currentPage = 1;
	let itemsPerPage = 100;

	$: totalPages = Math.ceil(filteredTransactions.length / itemsPerPage);

	$: paginatedTransactions = filteredTransactions.slice(
		(currentPage - 1) * itemsPerPage,
		currentPage * itemsPerPage
	);

	async function setTransactions(data) {
		Transactions = [...data]; // Ensure reactivity
	}

	onMount(async () => {
		await Session.handleSession();
		if (Session.SessionId) {
			await handleGetTransactions(Session.SessionId, setTransactions);
		}
		isLoading = false;
	});

	function formatTransactionDate(date, accuracy) {
		if (!date) return '';

		const parsedDate = moment.utc(date, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);

		if (!parsedDate.isValid()) {
			console.warn(`Invalid date format received: ${date}`);
			return 'Invalid Date';
		}

		switch (accuracy?.toLowerCase()) {
			case 'd': return parsedDate.format('YYYY-MM-DD');
			case 'm': return parsedDate.format('YYYY-MM');
			case 'y': return parsedDate.format('YYYY');
			default: return parsedDate.format('YYYY-MM-DD');
		}
	}

	function truncateText(text, maxLength = 25) {
		if (!text) return "";
		return text.length > maxLength ? text.substring(0, maxLength) + "…" : text;
	}

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	// Updated filteredTransactions to include transactionId and nola_id in the search string
	$: filteredTransactions = Transactions
		.filter(transaction => {
			const fullTransaction = `
				${transaction.Sellers} 
				${transaction.Buyers} 
				${transaction.Notary} 
				${transaction.TransactionId} 
				${transaction.nola_id}
				${transaction.TransactionType}
			`.toLowerCase();
			return fullTransaction.includes(searchQuery.toLowerCase());
		})
		.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Handle sorting for dates
			if (sortColumn === 'date_circa') {
				valueA = a.date_circa ? new Date(a.date_circa) : new Date(0);
				valueB = b.date_circa ? new Date(b.date_circa) : new Date(0);
			}

			// Handle sorting for numbers
			if (sortColumn === 'TotalPrice') {
				valueA = parseFloat(a.TotalPrice) || 0;
				valueB = parseFloat(b.TotalPrice) || 0;
			}

			// Convert strings to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			// Primary sort by the selected column
			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;

			// Secondary sort by date_circa
			const dateA = a.date_circa ? new Date(a.date_circa) : new Date(0);
			const dateB = b.date_circa ? new Date(b.date_circa) : new Date(0);
			if (dateA < dateB) return sortAscending ? -1 : 1;
			if (dateA > dateB) return sortAscending ? 1 : -1;

			return 0;
		});
	
	function addTransaction() {
		window.location.href = '/Admin/Transaction?transactionId=';
	}

	function goToPage(page) {
		if (page >= 1 && page <= totalPages) {
			currentPage = page;
		}
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
				<h3 class="title is-2">List of Transactions</h3>
				<button class="button is-primary" on:click={addTransaction}>Add Transaction</button>
			</div>
			
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} on:input={() => currentPage = 1} placeholder="Search by name or location" />
					</div>
				</div>
			</form>
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
						<th on:click={() => toggleSort('date_circa')}>Date</th>
						<th on:click={() => toggleSort('TransactionType')}>Transaction Type</th>
						<th on:click={() => toggleSort('Notary')}>Notary</th>
						<th on:click={() => toggleSort('Sellers')}>Seller</th>
						<th on:click={() => toggleSort('Buyers')}>Buyer</th>
					</tr>
				</thead>
				<tbody>
					{#each paginatedTransactions as transaction}
						<tr on:click={() => window.open(`/Admin/Transaction?TransactionId=${encodeURIComponent(transaction.TransactionId)}`, '_blank')}>
							
							<td>{formatTransactionDate(transaction.date_circa, transaction.date_accuracy)}</td>
							<td>{transaction.TransactionType || ''}</td>
							<td title={`${transaction.Notary || ''}`} >
								{truncateText(`${transaction.Notary || ''}`)}
							</td>
							<td title={`${transaction.Sellers || ''}`} >
								{truncateText(`${transaction.Sellers || ''}`)}
							</td>
							<td title={`${transaction.Buyers || ''}`} >
								{truncateText(`${transaction.Buyers || ''}`)}
							</td>
							
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="pagination">
				<button class="button" on:click={() => goToPage(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
				<span>Page {currentPage} of {totalPages}</span>
				<button class="button" on:click={() => goToPage(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
			</div>
		</div>
	</div>
{/if}
